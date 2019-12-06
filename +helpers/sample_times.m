function t = sample_times(data, fs)
% sample_times(data, fs)
%
% returns a vector of the time (in seconds) corresponding to each sample
% in <data>
%
% Input:
%     data - a numpy array (1D) of continuous voltage values
%     fs   - the sampling rate of the data in Hz
%
    len = numel(data);
    t = linspace(0, len / fs, len);
end
