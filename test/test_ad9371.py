import heapq
import test.rf.spec as spec
import time
from os import listdir
from os.path import dirname, join, realpath

import adi
import numpy as np
import pytest
from scipy import signal

hardware = "ad9371"
classname = "adi.ad9371"

profile_path = dirname(realpath(__file__)) + "/ad9371_5_profiles/"
test_profiles = [join(profile_path, f) for f in listdir(profile_path)]

params = dict(
    one_cw_tone_manual=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="manual",
        rx_hardwaregain_chan0=10,
        rx_hardwaregain_chan1=10,
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=0,
        rx_temp_comp_gain_chan1=0,
        tx_hardwaregain_chan0=0,
        tx_hardwaregain_chan1=0,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
    one_cw_tone_auto=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="automatic",
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=0,
        rx_temp_comp_gain_chan1=0,
        tx_hardwaregain_chan0=-10,
        tx_hardwaregain_chan1=-10,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
    change_attenuation_5dB_manual=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="manual",
        rx_hardwaregain_chan0=10,
        rx_hardwaregain_chan1=10,
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=0,
        rx_temp_comp_gain_chan1=0,
        tx_hardwaregain_chan0=-5,
        tx_hardwaregain_chan1=-5,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
    change_attenuation_10dB_manual=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="manual",
        rx_hardwaregain_chan0=10,
        rx_hardwaregain_chan1=10,
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=0,
        rx_temp_comp_gain_chan1=0,
        tx_hardwaregain_chan0=-10,
        tx_hardwaregain_chan1=-10,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
    change_attenuation_0dB_auto=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="automatic",
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=0,
        rx_temp_comp_gain_chan1=0,
        tx_hardwaregain_chan0=0,
        tx_hardwaregain_chan1=0,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
    change_attenuation_20dB_auto=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="automatic",
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=0,
        rx_temp_comp_gain_chan1=0,
        tx_hardwaregain_chan0=-20,
        tx_hardwaregain_chan1=-20,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
    change_rf_gain_0dB_manual=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="manual",
        rx_hardwaregain_chan0=0,
        rx_hardwaregain_chan1=0,
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=0,
        rx_temp_comp_gain_chan1=0,
        tx_hardwaregain_chan0=0,
        tx_hardwaregain_chan1=0,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
    change_rf_gain_20dB_manual=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="manual",
        rx_hardwaregain_chan0=20,
        rx_hardwaregain_chan1=20,
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=0,
        rx_temp_comp_gain_chan1=0,
        tx_hardwaregain_chan0=0,
        tx_hardwaregain_chan1=0,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
    change_temp_gain_up=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="manual",
        rx_hardwaregain_chan0=10,
        rx_hardwaregain_chan1=10,
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=3,
        rx_temp_comp_gain_chan1=3,
        tx_hardwaregain_chan0=0,
        tx_hardwaregain_chan1=0,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
    change_temp_gain_down=dict(
        ensm_mode="radio_on",
        tx_lo=2500000000,
        rx_lo=2500000000,
        gain_control_mode="manual",
        rx_hardwaregain_chan0=10,
        rx_hardwaregain_chan1=10,
        rx_quadrature_tracking_en_chan0=1,
        rx_quadrature_tracking_en_chan1=1,
        rx_temp_comp_gain_chan0=-3,
        rx_temp_comp_gain_chan1=-3,
        tx_hardwaregain_chan0=0,
        tx_hardwaregain_chan1=0,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
    ),
)

params_obs = [
    dict(  # Obs/Sniffer Manual Profile
        ensm_mode="radio_on",
        tx_hardwaregain_chan0=0,
        tx_hardwaregain_chan1=0,
        tx_quadrature_tracking_en_chan0=1,
        tx_quadrature_tracking_en_chan1=1,
        sn_lo=2500000000,
        obs_rf_port_select="ORX1_TX_LO",  # Can be parametrized
        obs_gain_control_mode="manual",
        obs_hardwaregain=0,
        obs_temp_comp_gain=0,
        obs_quadrature_tracking_en=1,
        # Obs/Snf gain control sync pulse=unchecked
    )
]


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol",
    [
        ("tx_hardwaregain_chan0", -41.95, 0.0, 0.05, 0.05),
        ("tx_hardwaregain_chan1", -41.95, 0.0, 0.05, 0.05),
        ("rx_lo", 70000000, 6000000000, 1000, 0),
        ("rx_lo", 70000000, 6000000000, 1000, 0),
    ],
)
def test_ad9371_attr(
    test_attribute_single_value, iio_uri, classname, attr, start, stop, step, tol
):
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol)


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", range(2))
def test_ad9371_rx_data(test_dma_rx, iio_uri, classname, channel):
    test_dma_rx(iio_uri, classname, channel)


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1])
@pytest.mark.parametrize(
    "param_set, frequency, scale, peak_min",
    [
        (params["one_cw_tone_manual"], 2000000, 0.5, -13),
        (params["one_cw_tone_manual"], 2000000, 0.12, -25),
        (params["one_cw_tone_manual"], 2000000, 0.25, -19),
        (params["one_cw_tone_auto"], 1000000, 0.12, -14.7),
        (params["one_cw_tone_auto"], 2000000, 0.12, -14.7),
        (params["one_cw_tone_auto"], 500000, 0.12, -14.7),
        (params["change_attenuation_5dB_manual"], 2000000, 0.25, -23.8),
        (params["change_attenuation_10dB_manual"], 2000000, 0.25, -28.75),
        (params["change_attenuation_0dB_auto"], 1000000, 0.12, -9),
        (params["change_attenuation_20dB_auto"], 1000000, 0.12, -24.7),
        (params["change_rf_gain_0dB_manual"], 2000000, 0.25, -29),
        (params["change_rf_gain_20dB_manual"], 2000000, 0.25, -9),
        (params["change_temp_gain_up"], 2000000, 0.25, -16),
        (params["change_temp_gain_down"], 2000000, 0.25, -22),
        # peak_min when the ADRV9371 setup has a splitter between RX and ORX
        # (params["one_cw_tone_manual"], 2000000, 0.5, -33),
        # (params["one_cw_tone_manual"], 2000000, 0.12, -45),
        # (params["one_cw_tone_manual"], 2000000, 0.25, -39),
        # (params["one_cw_tone_auto"], 1000000, 0.12, -34.7),
        # (params["one_cw_tone_auto"], 2000000, 0.12, -34.7),
        # (params["one_cw_tone_auto"], 500000, 0.12, -34.7),
        # (params["change_attenuation_5dB_manual"], 2000000, 0.25, -43.8),
        # (params["change_attenuation_10dB_manual"], 2000000, 0.25, -48.75),
        # (params["change_attenuation_0dB_auto"], 1000000, 0.12, -29),
        # (params["change_attenuation_20dB_auto"], 1000000, 0.12, -44.7),
        # (params["change_rf_gain_0dB_manual"], 2000000, 0.25, -49),
        # (params["change_rf_gain_20dB_manual"], 2000000, 0.25, -29),
        # (params["change_temp_gain_up"], 2000000, 0.25, -36),
        # (params["change_temp_gain_down"], 2000000, 0.25, -42),
    ],
)
def test_ad9371_dds_loopback(
    test_dds_loopback,
    iio_uri,
    classname,
    param_set,
    channel,
    frequency,
    scale,
    peak_min,
):
    test_dds_loopback(
        iio_uri, classname, param_set, channel, frequency, scale, peak_min
    )


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1])
@pytest.mark.parametrize(
    "param_set, frequency1, scale1, peak_min1, frequency2, scale2, peak_min2",
    [(params["one_cw_tone_auto"], 1000000, 0.06, -21, 2000000, 0.12, -15)],
)
def test_ad9371_two_tone_loopback(
    iio_uri,
    classname,
    channel,
    param_set,
    frequency1,
    scale1,
    peak_min1,
    frequency2,
    scale2,
    peak_min2,
):
    # See if we can tone using DMAs
    sdr = eval(classname + "(uri='" + iio_uri + "')")
    # Set custom device parameters
    for p in param_set.keys():
        setattr(sdr, p, param_set[p])
    # Set common buffer settings
    sdr.tx_cyclic_buffer = True
    N = 2 ** 14
    # Create a sinewave waveform
    if hasattr(sdr, "sample_rate"):
        RXFS = int(sdr.sample_rate)
    else:
        RXFS = int(sdr.rx_sample_rate)

    sdr.rx_enabled_channels = [channel]
    sdr.rx_buffer_size = N * 2 * len(sdr.rx_enabled_channels)
    sdr.dds_dual_tone(frequency1, scale1, frequency2, scale2, channel)

    # Pass through SDR
    try:
        for _ in range(10):  # Wait
            data = sdr.rx()
    except Exception as e:
        del sdr
        raise Exception(e)
    del sdr
    tone_peaks, tone_freqs = spec.spec_est(data, fs=RXFS, ref=2 ** 15)
    indx = heapq.nlargest(2, range(len(tone_peaks)), tone_peaks.__getitem__)
    print("Peak 1: " + str(tone_peaks[indx[0]]) + " @ " + str(tone_freqs[indx[0]]))
    print("Peak 2: " + str(tone_peaks[indx[1]]) + " @ " + str(tone_freqs[indx[1]]))

    try:
        if (abs(frequency1 - tone_freqs[indx[0]]) <= (frequency1 * 0.01)) and (
            abs(frequency2 - tone_freqs[indx[1]]) <= (frequency2 * 0.01)
        ):
            diff1 = np.abs(tone_freqs[indx[0]] - frequency1)
            diff2 = np.abs(tone_freqs[indx[1]] - frequency2)
            # print(frequency1, frequency2)
            # print(tone_freqs[indx[0]], tone_freqs[indx[1]])
            # print(tone_peaks[indx[0]], tone_peaks[indx[1]])
            # print(diff1, diff2)
            assert (frequency1 * 0.01) > diff1
            assert (frequency2 * 0.01) > diff2
            assert tone_peaks[indx[0]] > peak_min1
            assert tone_peaks[indx[1]] > peak_min2
        elif (abs(frequency2 - tone_freqs[indx[0]]) <= (frequency2 * 0.01)) and (
            abs(frequency1 - tone_freqs[indx[1]]) <= (frequency1 * 0.01)
        ):
            diff1 = np.abs(tone_freqs[indx[0]] - frequency2)
            diff2 = np.abs(tone_freqs[indx[1]] - frequency1)
            # print(frequency1, frequency2)
            # print(tone_freqs[indx[0]], tone_freqs[indx[1]])
            # print(tone_peaks[indx[0]], tone_peaks[indx[1]])
            # print(diff1, diff2)
            assert (frequency2 * 0.01) > diff1
            assert (frequency1 * 0.01) > diff2
            assert tone_peaks[indx[1]] > peak_min1
            assert tone_peaks[indx[0]] > peak_min2
    except Exception as e:
        raise Exception(e)


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1])
@pytest.mark.parametrize(
    "param_set, dds_scale, min_rssi, max_rssi",
    [
        (params["one_cw_tone_manual"], 0.5, 8.5, 9.5),
        (params["one_cw_tone_manual"], 0.12, 20.5, 21.5),
        (params["one_cw_tone_manual"], 0.25, 14.5, 15.5),
        (params["one_cw_tone_auto"], 0.12, 10.5, 11.5),
        (params["change_attenuation_5dB_manual"], 0.25, 19.5, 20.5),
        (params["change_attenuation_10dB_manual"], 0.25, 24.25, 25.25),
        (params["change_attenuation_0dB_auto"], 0.12, 4.75, 5.75),
        (params["change_attenuation_20dB_auto"], 0.12, 20.25, 21.5),
        (params["change_rf_gain_0dB_manual"], 0.25, 24.75, 26),
        (params["change_rf_gain_20dB_manual"], 0.25, 5, 6),
        (params["change_temp_gain_up"], 0.25, 14.5, 15.5),
        (params["change_temp_gain_down"], 0.25, 14.5, 15.5),
    ],
)
def test_ad9371_dds_gain_check_vary_power(
    test_gain_check,
    iio_uri,
    classname,
    channel,
    param_set,
    dds_scale,
    min_rssi,
    max_rssi,
):
    test_gain_check(
        iio_uri, classname, channel, param_set, dds_scale, min_rssi, max_rssi
    )


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1])
@pytest.mark.parametrize(
    "param_set",
    [
        params["one_cw_tone_manual"],
        params["one_cw_tone_auto"],
        params["change_attenuation_5dB_manual"],
        params["change_attenuation_10dB_manual"],
        params["change_attenuation_0dB_auto"],
        params["change_attenuation_20dB_auto"],
        params["change_rf_gain_0dB_manual"],
        params["change_rf_gain_20dB_manual"],
        params["change_temp_gain_up"],
        params["change_temp_gain_down"],
    ],
)
@pytest.mark.parametrize("sfdr_min", [40])
def test_ad9371_sfdr(test_sfdr, iio_uri, classname, channel, param_set, sfdr_min):
    test_sfdr(iio_uri, classname, channel, param_set, sfdr_min)


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("attr", ["profile"])
@pytest.mark.parametrize(
    "files", test_profiles,
)
def test_ad9371_profile_write(
    test_attribute_write_only_str, iio_uri, classname, attr, files
):
    test_attribute_write_only_str(iio_uri, classname, attr, files)
