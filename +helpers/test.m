function test()
param_file = './data/params.json';
events_file = './data/events.csv';
data_file = './data/continuous1.dat';
ts_file = './data/timestamps1.dat';

params = helpers.read_parameter_file(param_file);

[labels, events] = helpers.read_event_file(events_file);

data = helpers.read_data_file(data_file);
ts = helpers.read_data_file(ts_file);

helpers.plot_all(data, params, ts, events, labels);
end