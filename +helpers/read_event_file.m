function [labels, events] = read_event_file(filepath)
    d = readmatrix(filepath);
    labels = d(:,1);
    events = d(:,2);
end
