function plot_all(data, params, ts, events, labels)
% plot_all(data, params, ts, events, labels)
%
% plot evenything!
%
% Input:
%     data   - 1D array of continuous voltage values
%     params - a struct of experimental parameters for this data
%              as returned by read_parameter_file()
%     ts     - 1D array of spike timestamps (in seconds)
%     events - 1D array of event timestamps (in seconds)
%     labels - 1D array of event labels

    t = helpers.sample_times(data, params.sample_rate);

    ax = axes();

    plot(t, data, 'Parent', ax);

    hold('on');

    % plot a black "." at the time of each spike at a y-value of 1.0 (which in
    % this data is the peak amplitude of each spike)
    plot(ts, ones(numel(ts)), 'k.', 'Parent', ax);

    % make a list of color names (should be longer than the number of labels)
    % so that the lines for each event type show up in the same color
    colors = ['b','g','r','c','m','y'];

    % list of the unique event labels
    ulab = unique(labels);

    % precompute the y-values for our vertical line (data range +- 5%)
    mx = max(data);
    mn = min(data);
    pad = (mx - mn) * 0.05;
    mx = mx + pad;
    mn = mn - pad;

    % iterate over label,color pairs
    for k = 1:numel(ulab)

        % find all events of the current type <ulab(k)>
        b = labels == ulab(k);
        n = sum(b);

        % plot a vertical line at the time at which each event of type <ulab(k)>
        % occured where the x-values are of the form:
        %
        % x1, x2, x3...
        % x1, x2, x3...
        %
        % And the y-values are of the form:
        % y1, y1, y1...
        % y2, y2, y2
        plot(...
            [events(b)'; events(b)'],...
            [repmat(mn, 1, n); repmat(mx, 1, n)],...
            colors(k),...
            'Parent', ax...
        );
    end

end
