from .__init__ import *
from tqdm import trange
from .tools import check_dimension


class MSD(object):
    def __init__(self, position: NDArray):
        self.axis_dict = {"lag": 0, "N_particle": 1, "pos": -1}
        self.position = check_dimension(position, dim=3)
        self.kwrgs_it = {"desc": " MSD  (STEP) ", "ncols": 70, "ascii": True}
        self.N = self.position.shape[0]

    # User function
    def get_msd(self, fft: bool = True) -> NDArray[np.float64]:
        """Get MSD

        Calculate the msd data and return it with method and fft

        Args:
            position (np.ndarray)   :  Data of Particle's position in each lag time
            method (str, optional)  :  default = 'window'        (window or direct)
            fft (bool, optional)    :  default = True

        Returns:
            np.ndarray: _description_
        """
        if fft:
            self.msd_data = self.__get_msd_fft()
        else:
            self.msd_data = self.__get_msd_window()

        return self.msd_data

    # window method with non-FFT
    def __get_msd_window(self) -> NDArray[np.float64]:
        """MSD - Window Method with non-FFT

        Calculate the MSD list with linear loop with numpy function

        Time complexity : O(N**2)

        Args:
            position (np.ndarray): Data of Particle's position in each lag time
                - shape = [Number of lag, Number of particle, Coordinate data]

        Returns:
            list[float]: MSD data of each lag time
        """
        msd_list = np.zeros(self.position.shape[:2])
        for lag in trange(1, self.N, **self.kwrgs_it):
            diff_position = self.position[lag:] - self.position[:-lag]
            distance = self.__square_sum_position(diff_position)
            msd_list[lag, :] = np.mean(distance, axis=self.axis_dict["lag"])
        return self.__mean_msd_list(msd_list=msd_list)

    # window method with FFT
    def __get_msd_fft(self) -> NDArray[np.float64]:
        """MSD - Window method wit FFT

        Calculate the MSD list with linear loop with numpy function

        Time complexity : O(N logN)

        Args:
            position (np.ndarray): Data of Particle's position in each lag time
                - shape = [Number of lag, Number of particle, Coordinate data]

        Returns:
            list[float]: MSD data of each lag time
        """
        S_1 = self.__get_S_1()
        S_2 = self.__auto_correlation()
        msd_list = np.subtract(S_1, 2.0 * S_2)
        return self.__mean_msd_list(msd_list=msd_list)

    def __get_S_1(self) -> NDArray[np.float64]:
        empty_matrix = np.zeros(self.position.shape[:2])
        D = self.__square_sum_position(self.position)
        D = np.append(D, empty_matrix, axis=self.axis_dict["lag"])
        Q = 2.0 * np.sum(D, axis=self.axis_dict["lag"])
        S_1 = empty_matrix
        for m in trange(self.N, **self.kwrgs_it):
            Q -= D[m - 1, :] + D[self.N - m, :]
            S_1[m, :] = Q / (self.N - m)
        return S_1

    # get S2 for FFT
    def __auto_correlation(self) -> NDArray[np.float64]:
        X = np.fft.fft(self.position, n=2 * self.N, axis=self.axis_dict["lag"])
        dot_X = X * X.conjugate()
        x = np.fft.ifft(dot_X, axis=self.axis_dict["lag"])
        x = x[: self.N].real
        x = x.sum(axis=self.axis_dict["pos"])
        n = np.arange(self.N, 0, -1)
        return x / n[:, np.newaxis]

    # do square and sum about position
    def __square_sum_position(self, position_data) -> NDArray[np.float64]:
        return np.square(position_data).sum(axis=self.axis_dict["pos"])

    # do mean about msd list
    def __mean_msd_list(self, msd_list) -> NDArray[np.float64]:
        return msd_list.mean(axis=self.axis_dict["N_particle"])

    # plot the data
    def plot_msd(self, time_step: float = 1, *args, **kwargs):
        lagtime = len(self.position)
        x = np.arange(0, lagtime * time_step, time_step)
        y = self.msd_data
        plt.plot(x, y, *args, **kwargs)
        plt.show()
