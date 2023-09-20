
function data = filterDataMano(data,fs)
tVec = 1/fs:1/fs:size(data,2)/fs;
%% Baseline removal 
% tic

winSpan = fs*60*1;  %% was 10 - worked well
winSpan = fs*60*0.5;
sideBase = 'bottom';
% upd = textprogressbar(size(data.sig,1));
env_baseline = zeros(size(data));
for i = 1:size(data,1)
%     i
    if sum(data(i,:))==0 % if signal 0 there is no need for baseline est
%         env_baseline(i,:)=0;
    else
    env_baseline(i,:) = env_secant(tVec, data(i,:), winSpan, sideBase);
%     upd(i);
    end
end
x_env = data-env_baseline;


%% Removing synchronous noise 

medianSynchSignal = median(x_env,1); 
syn_curve = repmat(medianSynchSignal , size(x_env, 1), 1); % was part of algo
x1 = x_env - syn_curve ;

x1=x_env;

%% Spatiotemporal filter 


%Temporal filter - Savitzky-Golay filtering
p_order=3;
framelen=1+fs*5.4;
framelen=fs*7.9;
% K2 = transpose(sgolayfilt(K1',p_order,framelen));
K22 = transpose(sgolayfilt(x1',p_order,framelen));
data = wiener2(K22,[5 fs*0.5]);
% data = K22;





end





function [env] = env_secant(x_data, y_data, view, side)
% Function call: env_secant(x_data, y_data, view, side)
% Calculates the top envelope of data <y_data> over <x_data>.
% Method used: 'secant-method'
% env_secant() observates the max. slope of about <view> points,
% and joints them to the resulting envelope.
% An interpolation over original x-values is done finally.
% <side> ('top' or 'bottom') defines which side to evolve.

    if nargin == 0
        test( false );
        test( true );
        return
    end

    if nargin < 4
        error( '%s needs at least 4 input arguments!', mfilename );
    end

    assert( isnumeric(view) && isscalar(view) && view > 1, ...
           'Parameter <view> must be a value greater than 1!' );
    assert( isvector(x_data) && isnumeric(x_data) && all( isfinite( x_data ) ), ...
           'Parameter <x_data> has to be of vector type, holding finite numeric values!' );
    assert( isvector(y_data) && isnumeric(y_data) && all( isfinite( y_data ) ), ...
           'Parameter <y_data> has to be of vector type, holding finite numeric values!' );
    assert( isequal( size(x_data), size(y_data) ), ...
           'Parameters <x_data> and <y_data> must have same size and dimension!' );
    assert( ischar(side), ...
            'Parameter <side> must be ''top'' or ''bottom''!' );

    switch lower( side )
        case 'top'
            side = 1;
        case 'bottom'
            side = -1;
        otherwise
            error( 'Parameter <side> must be ''top'' or ''bottom''!' );
    end

    sz = size( x_data );

    x_data = x_data(:);
    x_diff = diff( x_data );
    x_diff = [min(x_diff), max(x_diff)];
    assert( x_diff(1) > 0, '<x_data> must be monotonic increasing!' );

    y_data = y_data(:);
    data_len = length( y_data );
    x_new = [];
    y_new = [];

    if diff( x_diff ) < eps( max(x_data) ) + eps( min(x_data) )
        % x_data is equidistant
        search_fcn = @( y_data, ii, i ) ...
                     max( ( y_data(ii) - y_data(i) ) ./ (ii-i)' * side );
    else
        % x_data is not equidistant
        search_fcn = @( y_data, ii, i ) ...
                     max( ( y_data(ii) - y_data(i) ) ./ ( x_data(ii) - x_data(i) ) * side );
    end


    i = 1;
    while i < data_len;
        ii = i+1:min( i + view, data_len );
        [ m, idx ] = search_fcn( y_data, ii, i );

        % New max. slope: store new "observation point"
        i = i + idx;
        x_new(end+1) = x_data(i);
        y_new(end+1) = y_data(i);
    end;

    env = interp1( x_new, y_new, x_data, 'linear', 'extrap' );
    env = reshape( env, sz );
end




function test( flagMonotonic )
    npts = 100000;
    y_data = cumsum( randn( npts, 1 ) ) .* cos( (1:npts)/50 )' + 100 * cos( (1:npts)/6000 )';
    if flagMonotonic
        x_data = (1:npts)' + 10;
    else
        x_diff = rand( size( y_data ) );
        x_data = cumsum( x_diff );
    end

    view = ceil( npts * 0.01 ); % 1 Percent of total length
    env_up = env_secant( x_data, y_data, view, 'top' );
    env_lo = env_secant( x_data, y_data, view, 'bottom' );

    figure
    plot( x_data, y_data, '-', 'Color', 0.8 * ones(3,1) );
    hold all
    h(1) = plot( x_data, env_up, 'b-', 'DisplayName', 'top' );
    h(2) = plot( x_data, env_lo, 'g-', 'DisplayName', 'bottom' );

    grid
    legend( 'show', h )

    
end
