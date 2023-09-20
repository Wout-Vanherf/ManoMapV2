classdef manoMap < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        ManoMapUIFigure               matlab.ui.Figure
        LoaddataButton                matlab.ui.control.Button
        Label                         matlab.ui.control.Label
        PlotimageButton               matlab.ui.control.Button
        PlotsignalsButton             matlab.ui.control.Button
        ExportButton                  matlab.ui.control.Button
        StartEndTimeEditFieldLabel    matlab.ui.control.Label
        EditField_StartTime           matlab.ui.control.NumericEditField
        EditField_EndTime             matlab.ui.control.NumericEditField
        ColourLimitsEditFieldLabel    matlab.ui.control.Label
        ColourLimitsEditField_lwr     matlab.ui.control.NumericEditField
        ColourLimitsEditField_higher  matlab.ui.control.NumericEditField
        Y_offsetEditFieldLabel        matlab.ui.control.Label
        Y_offsetEditField             matlab.ui.control.NumericEditField
        DetectEventsButton            matlab.ui.control.Button
        DetectionThresholdmmHgLabel   matlab.ui.control.Label
        DetectionThresholdmmHgEditField  matlab.ui.control.NumericEditField
        ExitButton                    matlab.ui.control.Button
        MedianfilteringacrosschannelsButton  matlab.ui.control.Button
        NormalfiltereddataButton      matlab.ui.control.Button
        UIAxes                        matlab.ui.control.UIAxes
        StartEndCameraEditFieldLabel  matlab.ui.control.Label %field to limit to a range of output
        EditField_StartSensor         matlab.ui.control.NumericEditField
        EditField_EndSensor           matlab.ui.control.NumericEditField
        AddEventFieldTimeLabel        matlab.ui.control.Label
        AddEventTimeField             matlab.ui.control.NumericEditField
        AddEventFieldNameLabel        matlab.ui.control.Label
        AddEventNameField
        AddEventButton                matlab.ui.control.Button                         
    end
    
    properties (Access = public)
        data % contains sig (filtered) and raw sig
        ClstMetrics %Clustered metrics
        fileName %name of file analyse
        elecSpacing %elecspacing
    end
    

    % Callbacks that handle component events
    methods (Access = private)

        % Button pushed function: LoaddataButton
        function LoaddataButtonPushed(app, event)
        %get file
%         cd E:\2021\Annelies_Leuven\Files_from_Leuven
        cla(app.UIAxes,"reset")
        app.LoaddataButton.BackgroundColor = [0.5, 0.5 0.5];
        app.Label.Text ='Loading data';
        [filename,pathname] = ...
        uigetfile({'*.txt';'*.mat'},'Select Any Dataset in The Desired Directory...');
%         filename = 'CM_20120414_Postmeal.txt';
%         pathname = 'E:\2021\Cam_cHRM-Pre-Op\Controls_29062021\Archive_controls\';
       
        if (filename ~= 0)
            filenameAll = sprintf('%s%s',pathname,filename);   %concatenate strings
        
        %Load data 
        choice = questdlg('Is this raw or marked data', ...
            'Select file type',...
            'Raw_Data_UoA_Flinders', 'Raw_Data_Leuven','Cancel','Raw_Data_UoA_Flinders');
        switch choice
            case 'Raw_Data_UoA_Flinders'
                loadData = transpose(dlmread(filenameAll));
                app.data.sig = loadData(3:end,:);
                app.data.rawData = app.data.sig;
                app.data.t=loadData(1,:);
                app.data.fs = round(1/(median(diff(app.data.t))));
                app.Label.Text = filename;
                app.elecSpacing = 1;
                 
%                  %filter data
%                  app.data.sig = filterDataMano(app.data.sig,app.data.fs);
                 
                 app.LoaddataButton.BackgroundColor =[0.39,0.83,0.07];
                 
                 app.EditField_EndTime.Value = app.data.t(end)/60;
                 app.EditField_StartTime.Value = app.data.t(1)/60;
                 app.ColourLimitsEditField_higher.Value = 60;
                 app.ColourLimitsEditField_lwr.Value = 0;
                 app.Y_offsetEditField.Value=50;
                 app.DetectionThresholdmmHgEditField.Value=10;
                 
                 app.fileName = filename;
                
            case 'Raw_Data_Leuven'
                loadData = transpose(dlmread(filenameAll));
                app.data.sig = loadData(2:end-1,:);
                app.data.rawData = app.data.sig;
                app.data.t=loadData(1,:);
                app.data.fs = round(1/(median(diff(app.data.t))));
                app.Label.Text = filename;
                app.elecSpacing = 5;

                 
                 app.LoaddataButton.BackgroundColor =[0.39,0.83,0.07];
                 
                 app.EditField_EndTime.Value = app.data.t(end)/60;
                 app.EditField_StartTime.Value = app.data.t(1)/60;
                 app.ColourLimitsEditField_higher.Value = 60;
                 app.ColourLimitsEditField_lwr.Value = 0;
                 app.Y_offsetEditField.Value=50;
                 app.DetectionThresholdmmHgEditField.Value=10;
                 
                 app.fileName = filename;

            case 'Cancel'
                fprintf('No Files were selected\n');
                msgbox('No file loaded')
        end
        
        else
            fprintf('No Files were selected\n');
            app.Label.Text ='No file was selected';
        end
        
        end

        % Button pushed function: PlotimageButton
        function PlotimageButtonPushed(app, event)
            if ~isempty(app.data)
                
            cla(app.UIAxes,'reset')
%             keyboard
            tVec = app.data.t;
            pltData = app.data.sig;
            pltData =imresize(pltData ,[size(app.data.sig,1),size(app.data.sig,2)*5]);
            fsNew = app.data.fs*5;
            tVec = tVec(1):1/fsNew:tVec(end); 
            tVec =tVec./60;  
            
            sigma = 0.5;
            pltData = imgaussfilt(pltData,sigma,'filtersize',[3 51]); % 5chans acorss ~20s
            
            imagesc(app.UIAxes,tVec ,1:size(app.data.sig,1),pltData);
            colormap(app.UIAxes,cmocean('thermal'))
            colorbar(app.UIAxes)
%             caxis(app.UIAxes,[0 60])
            caxis(app.UIAxes,[app.ColourLimitsEditField_lwr.Value app.ColourLimitsEditField_higher.Value])
                 
            xlabel(app.UIAxes,'Time (min)')
%             xlim(app.UIAxes,[tVec(1) tVec(end)])
            
            if isempty(app.EditField_StartTime.Value) && isempty(app.EditField_EndTime.Value)            
            app.EditField_StartTime.Value = tVec(1);
            app.EditField_EndTime.Value = tVec(end);
            end
            xlim(app.UIAxes,[app.EditField_StartTime.Value app.EditField_EndTime.Value])
            
            end
        end

        % Button pushed function: PlotsignalsButton
        function PlotsignalsButtonPushed(app, event)
            if ~isempty(app.data)
                if app.Y_offsetEditField.Value>2
            cla(app.UIAxes,'reset');
            hold(app.UIAxes,'on');
            x = app.data.sig; 
            %x = data.rawData; 
            fs = app.data.fs;
            tVec = app.data.t;
            RGB = cmocean('thermal',size(x,1)+15);
%             hLimP=50;
            hLimP=app.Y_offsetEditField.Value;
            for i =1:size(x,1)
            %         plot(t,x(i,:)+i*15,'color',RGB(i,:))
                ytickChannelPos(i)=hLimP*i*-1;
                ytickChan(i)=i;
                 plot(app.UIAxes,tVec/60,x(i,:)+ytickChannelPos(i),'color',RGB(i,:));

            end
            %     ax = gca;
            [~,II]=sort(ytickChannelPos);
            app.UIAxes.YTick=ytickChannelPos(II);
            app.UIAxes.YTickLabel=ytickChan(II);
            app.UIAxes.YLim=[ytickChannelPos(II(1))-70 ytickChannelPos(II(end))+70];
            app.UIAxes.XLim=[tVec(1)/60 tVec(end)/60];
            xlabel(app.UIAxes,'Time (min)');

            hold(app.UIAxes,'off');
            
            ylim(app.UIAxes,[ytickChannelPos(end)-50 ytickChannelPos(1)+max(x(1,:))]);
            
            if isempty(app.EditField_StartTime.Value) && isempty(app.EditField_EndTime.Value)            
            app.EditField_StartTime.Value = tVec(1);
            app.EditField_EndTime.Value = tVec(end);
            end
            xlim(app.UIAxes,[app.EditField_StartTime.Value app.EditField_EndTime.Value]);
            
                else
                    msgbox('Choose a larger y_offset');
                end
            end

        end

        % Add Event Function: AddEventButtonPushed
        function AddEventButtonPushed(app, event)
            if(isempty(app.AddEventNameField.Value) || isempty(app.AddEventTimeField.Value))
                msgbox('Fill in a time and name of the event');
            else
                %REDRAW WITH EVENT
                
            end
        end

        % Value changed function: EditField_StartTime
        function EditField_StartTimeValueChanged(app, event)
            value = app.EditField_StartTime.Value;
%             keyboard
            if value>app.EditField_EndTime.Value
               msgbox('Start time should be before end time') ;
            elseif value==app.EditField_EndTime.Value
                msgbox('Start time and end time cannot be the same') ;
            else
            xlim(app.UIAxes,[app.EditField_StartTime.Value app.EditField_EndTime.Value]);
            end
        end

        % Value changed function: EditField_EndTime
        function EditField_EndTimeValueChanged(app, event)
            value = app.EditField_EndTime.Value;
            if value<app.EditField_StartTime.Value
               msgbox('End time should be after start time') 
            elseif value==app.EditField_StartTime.Value
                msgbox('Start time and end time cannot be the same') 
            else
            xlim(app.UIAxes,[app.EditField_StartTime.Value app.EditField_EndTime.Value]);
            end
        end

        % Value changed function: EditField_StartSensor
        function EditField_StartSensorValueChanged(app, event)
            value = app.EditField_StartSensor.Value;
%             keyboard
            if value>app.EditField_EndSensor.Value
               msgbox('Start sensor should be before end sensor') ;
            else
            ylim(app.UIAxes,[app.EditField_StartSensor.Value app.EditField_EndSensor.Value]);
            end
        end

        % Value changed function: EditField_EndSensor
        function EditField_EndSensorValueChanged(app, event)
            value = app.EditField_EndSensor.Value;
%             keyboard
            if value<app.EditField_StartSensor.Value
               msgbox('End sensor should be after start sensor') ;
            else
            ylim(app.UIAxes,[app.EditField_StartSensor.Value app.EditField_EndSensor.Value]);
            end
        end

        % Value changed function: ColourLimitsEditField_lwr
        function ColourLimitsEditField_lwrValueChanged(app, event)
            value = app.ColourLimitsEditField_lwr.Value;
            if value>app.ColourLimitsEditField_higher.Value
               msgbox('Start colour should be before end colour') 
            elseif value==app.ColourLimitsEditField_higher.Value
                msgbox('Start colour and end colour cannot be the same') 
            else
            caxis(app.UIAxes,[app.ColourLimitsEditField_lwr.Value app.ColourLimitsEditField_higher.Value]);
            end
        end

        % Value changed function: ColourLimitsEditField_higher
        function ColourLimitsEditField_higherValueChanged(app, event)
            value = app.ColourLimitsEditField_higher.Value;
            if value<app.ColourLimitsEditField_lwr.Value
               msgbox('End colour should be after start colour') 
            elseif value==app.ColourLimitsEditField_lwr.Value
                msgbox('Start colour and end colour cannot be the same') 
            else
            caxis(app.UIAxes,[app.ColourLimitsEditField_lwr.Value app.ColourLimitsEditField_higher.Value]);
            end
        end

        % Value changed function: Y_offsetEditField
        function Y_offsetEditFieldValueChanged(app, event)
            value = app.Y_offsetEditField.Value;
            
            PlotsignalsButtonPushed(app, event)
        end

        % Button pushed function: DetectEventsButton
        function DetectEventsButtonPushed(app, event)

if ~isempty(app.data)
    
            Igaussian=app.data.sig;

            %% Detect Signals
            fprintf('Detection\n')
            thresh=5; 
            thresh = app.DetectionThresholdmmHgEditField.Value;
            
            BW = imbinarize(Igaussian,thresh);
            
            fprintf('Get Clustered Info\n')
            L = bwlabel(BW); %  Create a label matrix from this BW image.
            pixelIndexList = label2idx(L); % Get linear index of all pixels regions
            % figure, imagesc(L)
            [Clst,binDetectImg] = getChanIdxFrmt(Igaussian,L,pixelIndexList);


            %Compute Metrics 
            dataSig = Igaussian;

            for i =1:length(Clst)
                %get amplitude information 
                for j  = 1:size(Clst{i},1) %loop through markers
            %         fprintf('i: %d, j:%d\n',i,j)
                    if Clst{i}(j,2)+5<=size(dataSig,2) && Clst{i}(j,2)-5>=1
                        ampl(j) = max(dataSig(Clst{i}(j,1),Clst{i}(j,2)-5:Clst{i}(j,2)+5));
                    else
                        ampl(j)= dataSig(Clst{i}(j,1),Clst{i}(j,2));
                    end
                end
            %     amplProp(i) = mean(ampl); clear ampl
                amplProp(i) = prctile(ampl,75); clear ampl
                
                
                %get velocity estimates
                timeDiff = diff(Clst{i}(:,2));
                dirEst = sign(timeDiff); %postive - antegrade, negative - retrograde
                P = polyfit(Clst{i}(:,2),Clst{i}(:,1),1); % to enforce only ante vs retro
                if P(1) > 0 %antegrade
                    dirProp(i) = 1;
                elseif P(1)<0 %retrograde
                    dirProp(i) = 2;
                end
                
                timeDiff(timeDiff==0)=[];%remove 0 time diff values
                speed(i) = app.elecSpacing/median(abs(timeDiff./10));
                if speed(i) == Inf
                    keyboard % should not happen now
                end 
            %     keyboard
                
                %get length of travel
                lengthTrvl(i) = length(Clst{i});
            %     mean time
                meanTimeProp(i) = mean(app.data.t(Clst{i}(:,2)));
                startTimeProp(i) = min(app.data.t(Clst{i}(:,2)));
                
            end
            
            
            %% Figure plotting
            h1=uifigure();
            h1.Icon='logo.png';
            axPlt = gca(h1);
            hold(axPlt,'on')
            h=imagesc(axPlt,app.data.t/60,1:size(app.data.sig,1),app.data.sig);
            for i = 1:length(Clst);
                if dirProp(i)==1
                    plot(axPlt, app.data.t(Clst{i}(:,2))./60,Clst{i}(:,1),'b-');
                elseif dirProp(i)==2
                    plot(axPlt, app.data.t(Clst{i}(:,2))./60,Clst{i}(:,1),'r-');
                end
                    
            end
            axPlt.YDir='reverse';
            xlim(axPlt,[app.data.t(1) app.data.t(end)]./60)
            ylim(axPlt,[1 size(dataSig,1)])
            colorbar(axPlt)
            colormap(axPlt,cmocean('thermal'))
            caxis(axPlt,[0 60])
            set(h, 'AlphaData', 0.5)
            xlabel(axPlt,'Time(min)')
            title(axPlt,sprintf('Threshold used: %3.2f mmHg', app.DetectionThresholdmmHgEditField.Value))
            
            app.ClstMetrics.Clst = Clst;
            app.ClstMetrics.dirProp = dirProp;
            app.ClstMetrics.lengthTrvl = lengthTrvl;
            app.ClstMetrics.speed = speed;
            app.ClstMetrics.amplProp = amplProp;
            app.ClstMetrics.startTimeProp=startTimeProp;
            app.ClstMetrics.Thresh = app.DetectionThresholdmmHgEditField.Value;

end


        end

        % Value changed function: DetectionThresholdmmHgEditField
        function DetectionThresholdmmHgEditFieldValueChanged(app, event)
            value = app.DetectionThresholdmmHgEditField.Value;
            %DetectEventsButtonPushed(app, event); 
        end

        % Button pushed function: ExportButton
        function ExportButtonPushed(app, event)

        if ~isempty(app.ClstMetrics)

            Cluster = app.ClstMetrics.Clst;
           
            startTime = app.ClstMetrics.startTimeProp;
            directionProp = app.ClstMetrics.dirProp ;
            lengthTravel=app.ClstMetrics.lengthTrvl ;
            amplitude=app.ClstMetrics.amplProp;
            speed=app.ClstMetrics.speed;
            
%             sigFiltered = app.data.sig;
            
%             keyboard
            defaultFile = strcat(app.fileName(1:end-4),'_Metrics.xls');
            [fileXls,path,indx] = uiputfile(defaultFile);
            
            %write out excel file
%             fileXls = 'out.xls';
            if fileXls~=0
            disp(pwd)
            xlswrite(fileXls,cellstr(app.fileName),1,'A1'); %write filename
            xlswrite(fileXls,cellstr('Threshold used'),1,'A2'); %write Thresh
            xlswrite(fileXls,app.ClstMetrics.Thresh,1,'B2'); %write Thresh
            outTable = table([1:length(Cluster)]',startTime',directionProp',lengthTravel',amplitude',speed',...
                'VariableNames',{'ClusterNo','Start_Time_sec','Direction','LengthProp_cm','Amplitude_mmHg','Speed_cms'});
            writetable(outTable,fileXls,'Sheet',1,'Range','B3') 
            end
            
        %write out csv file
        txtFileOutput = Cluster;
%         fid = fopen(strcat('output\',fileloc{j}(end-29:end-4),'_WaveInfo.txt'),'w+');
        defaultFile = strcat(app.fileName(1:end-4),'_WaveInfo.csv');
        [fileWav,path,indx] = uiputfile(defaultFile);
        
        if fileWav~=0
%         fid = fopen('WaveInfo.txt','w+');
        fid = fopen(fileWav,'w+');
        fprintf(fid, '%s \n',app.fileName); 
        %     
        for k = 1:length(txtFileOutput)
            fprintf(fid, '%d \n',k);
            for m = 1:length(txtFileOutput{k})
                 fprintf(fid, '%d \t %d \n', txtFileOutput{k}(m,1),txtFileOutput{k}(m,2));
            end
            fprintf(fid, '\n\n');
        end
        fclose(fid);
        end
        
        %Save Mat File
        disp('Saving mat file')
        defaultFile = strcat(app.fileName(1:end-4),'_MatFile.mat');
        [matFileSave,path,indx] = uiputfile(defaultFile);
        if matFileSave~=0
        Clust = app.ClstMetrics;
        fileNameOrig = app.fileName;
        save(matFileSave,"Clust","fileNameOrig","-mat")
        end
        
        end
        
        end

        % Button pushed function: ExitButton
        function ExitButtonPushed(app, event)
            app.delete;
        end
        
        % Window scroll wheel function: ManoMapUIFigure
        function ManoMapUIFigureWindowScrollWheel(app, event)
            verticalScrollAmount = event.VerticalScrollAmount;
            verticalScrollCount = event.VerticalScrollCount;

            %Check if in axis and then adjust controls
            cp = app.ManoMapUIFigure.CurrentSensor;
            isInAxes = cp(1) >= app.UIAxes.Position(1) && ...
            cp(1) <= sum(app.UIAxes.Position([1,3])) && ...
            cp(2) >= app.UIAxes.Position(2) && ...
            cp(2) <= sum(app.UIAxes.Position([2,4]));
            if isInAxes
                % Update displayed coordinates
                if ~isempty(app.data)
                    winSize = app.EditField_EndTime.Value - app.EditField_StartTime.Value;
                    ScrlSize = round(winSize/3) * verticalScrollCount*-1;

                    startAdd = app.EditField_StartTime.Value +ScrlSize;
                    endValAdd = app.EditField_EndTime.Value +ScrlSize;
                    if startAdd<0
                        startAdd = 0;
                        endValAdd = app.EditField_EndTime.Value;
                    end
                    if endValAdd > app.data.t(end)/60
                        endValAdd = app.data.t(end)/60;
                         startAdd = app.EditField_StartTime.Value;    
                    end
                    xlim(app.UIAxes,[startAdd endValAdd]);
                    app.EditField_StartTime.Value = startAdd;
                    app.EditField_EndTime.Value = endValAdd;
                    
                end
            else

            end

        end
        
        % Button pushed function: 
        function MedianfilteringacrosschannelsButtonPushed(app, event)
            sig = app.data.sig;
            sig1 = movmedian(sig,3,1);
            app.data.sig = sig1;
        end
        
        % Button pushed function: NormalfiltereddataButton
        function NormalfiltereddataButtonPushed(app, event)
            app.data.sig = filterDataMano(app.data.rawData,app.data.fs);
        end
        
    
    end
    

        
    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)
            
            % Create ManoMapUIFigure and hide until all components are created
            app.ManoMapUIFigure = uifigure('Visible', 'off');
            app.ManoMapUIFigure.Position = [100 100 696 531];
            app.ManoMapUIFigure.Name = 'ManoMap';
            app.ManoMapUIFigure.Icon = 'logo.png';
            app.ManoMapUIFigure.WindowScrollWheelFcn = createCallbackFcn(app, @ManoMapUIFigureWindowScrollWheel, true);

            % Create LoaddataButton
            app.LoaddataButton = uibutton(app.ManoMapUIFigure, 'push');
            app.LoaddataButton.ButtonPushedFcn = createCallbackFcn(app, @LoaddataButtonPushed, true);
            app.LoaddataButton.BackgroundColor = [0.902 0.902 0.902];
            app.LoaddataButton.FontColor = [0.149 0.149 0.149];
            app.LoaddataButton.Position = [31 481 118 31];
            app.LoaddataButton.Text = 'Load data';

            % Create Label
            app.Label = uilabel(app.ManoMapUIFigure);
            app.Label.Position = [151 487 399 25];
            app.Label.Text = '';

            % Create PlotimageButton
            app.PlotimageButton = uibutton(app.ManoMapUIFigure, 'push');
            app.PlotimageButton.ButtonPushedFcn = createCallbackFcn(app, @PlotimageButtonPushed, true);
            app.PlotimageButton.Position = [51 121 118 31];
            app.PlotimageButton.Text = 'Plot image';

            % Create PlotsignalsButton
            app.PlotsignalsButton = uibutton(app.ManoMapUIFigure, 'push');
            app.PlotsignalsButton.ButtonPushedFcn = createCallbackFcn(app, @PlotsignalsButtonPushed, true);
            app.PlotsignalsButton.Position = [302 121 118 31];
            app.PlotsignalsButton.Text = 'Plot signals';

            % Create ExportButton
            app.ExportButton = uibutton(app.ManoMapUIFigure, 'push');
            app.ExportButton.ButtonPushedFcn = createCallbackFcn(app, @ExportButtonPushed, true);
            app.ExportButton.Position = [526 59 118 31];
            app.ExportButton.Text = 'Export';

            % Create StartEndTimeEditFieldLabel
            app.StartEndTimeEditFieldLabel = uilabel(app.ManoMapUIFigure);
            app.StartEndTimeEditFieldLabel.HorizontalAlignment = 'right';
            app.StartEndTimeEditFieldLabel.Position = [34 63 86 22];
            app.StartEndTimeEditFieldLabel.Text = 'Start-End Time';

            % Create EditField_StartTime
            app.EditField_StartTime = uieditfield(app.ManoMapUIFigure, 'numeric');
            app.EditField_StartTime.ValueChangedFcn = createCallbackFcn(app, @EditField_StartTimeValueChanged, true);
            app.EditField_StartTime.Position = [121 61 38 29];

            % Create EditField_EndTime
            app.EditField_EndTime = uieditfield(app.ManoMapUIFigure, 'numeric');
            app.EditField_EndTime.ValueChangedFcn = createCallbackFcn(app, @EditField_EndTimeValueChanged, true);
            app.EditField_EndTime.Position = [175 62 38 29];

            % Create ColourLimitsEditFieldLabel
            app.ColourLimitsEditFieldLabel = uilabel(app.ManoMapUIFigure);
            app.ColourLimitsEditFieldLabel.HorizontalAlignment = 'right';
            app.ColourLimitsEditFieldLabel.Position = [32 16 76 22];
            app.ColourLimitsEditFieldLabel.Text = 'Colour Limits';

            % Create ColourLimitsEditField_lwr
            app.ColourLimitsEditField_lwr = uieditfield(app.ManoMapUIFigure, 'numeric');
            app.ColourLimitsEditField_lwr.ValueChangedFcn = createCallbackFcn(app, @ColourLimitsEditField_lwrValueChanged, true);
            app.ColourLimitsEditField_lwr.Position = [123 13 36 29];

            % Create ColourLimitsEditField_higher
            app.ColourLimitsEditField_higher = uieditfield(app.ManoMapUIFigure, 'numeric');
            app.ColourLimitsEditField_higher.ValueChangedFcn = createCallbackFcn(app, @ColourLimitsEditField_higherValueChanged, true);
            app.ColourLimitsEditField_higher.Position = [175 13 36 29];

            % Create Y_offsetEditFieldLabel
            app.Y_offsetEditFieldLabel = uilabel(app.ManoMapUIFigure);
            app.Y_offsetEditFieldLabel.HorizontalAlignment = 'right';
            app.Y_offsetEditFieldLabel.Position = [275 68 55 22];
            app.Y_offsetEditFieldLabel.Text = 'Y_offset';

            % Create Y_offsetEditField
            app.Y_offsetEditField = uieditfield(app.ManoMapUIFigure, 'numeric');
            app.Y_offsetEditField.ValueChangedFcn = createCallbackFcn(app, @Y_offsetEditFieldValueChanged, true);
            app.Y_offsetEditField.Position = [345 67 30 25];

            % Create DetectEventsButton
            app.DetectEventsButton = uibutton(app.ManoMapUIFigure, 'push');
            app.DetectEventsButton.ButtonPushedFcn = createCallbackFcn(app, @DetectEventsButtonPushed, true);
            app.DetectEventsButton.Position = [526 121 118 31];
            app.DetectEventsButton.Text = 'Detect Events';

            % Create DetectionThresholdmmHgLabel
            app.DetectionThresholdmmHgLabel = uilabel(app.ManoMapUIFigure);
            app.DetectionThresholdmmHgLabel.HorizontalAlignment = 'center';
            app.DetectionThresholdmmHgLabel.Position = [240 6 106 43];
            app.DetectionThresholdmmHgLabel.Text = {'Detection '; 'Threshold (mmHg)'};

            % Create DetectionThresholdmmHgEditField
            app.DetectionThresholdmmHgEditField = uieditfield(app.ManoMapUIFigure, 'numeric');
            app.DetectionThresholdmmHgEditField.ValueChangedFcn = createCallbackFcn(app, @DetectionThresholdmmHgEditFieldValueChanged, true);
            app.DetectionThresholdmmHgEditField.Position = [345 16 30 28];

            % Create ExitButton
            app.ExitButton = uibutton(app.ManoMapUIFigure, 'push');
            app.ExitButton.ButtonPushedFcn = createCallbackFcn(app, @ExitButtonPushed, true);
            app.ExitButton.Position = [526 7 118 31];
            app.ExitButton.Text = 'Exit';

            % Create MedianfilteringacrosschannelsButton
            app.MedianfilteringacrosschannelsButton = uibutton(app.ManoMapUIFigure, 'push');
            app.MedianfilteringacrosschannelsButton.ButtonPushedFcn = createCallbackFcn(app, @MedianfilteringacrosschannelsButtonPushed, true);
            app.MedianfilteringacrosschannelsButton.BackgroundColor = [0.651 0.651 0.651];
            app.MedianfilteringacrosschannelsButton.Position = [486 488 198 30];
            app.MedianfilteringacrosschannelsButton.Text = '2.Median filtering across channels';

            % Create NormalfiltereddataButton
            app.NormalfiltereddataButton = uibutton(app.ManoMapUIFigure, 'push');
            app.NormalfiltereddataButton.ButtonPushedFcn = createCallbackFcn(app, @NormalfiltereddataButtonPushed, true);
            app.NormalfiltereddataButton.BackgroundColor = [0.302 0.7451 0.9333];
            app.NormalfiltereddataButton.Position = [329 485 136 33];
            app.NormalfiltereddataButton.Text = '1.Normal filtered data';
            
            % Create UIAxes
            app.UIAxes = uiaxes(app.ManoMapUIFigure);
            title(app.UIAxes, 'ManoMap')
            xlabel(app.UIAxes, 'X')
            ylabel(app.UIAxes, 'Y')
            zlabel(app.UIAxes, 'Z')
            app.UIAxes.Position = [9 151 674 331];

            % Create StartEndCameraEditFieldLabel
            app.StartEndCameraEditFieldLabel = uilabel(app.ManoMapUIFigure);
            app.StartEndCameraEditFieldLabel.HorizontalAlignment = 'right';
            app.StartEndCameraEditFieldLabel.Position = [15 90 100 22];
            app.StartEndCameraEditFieldLabel.Text = 'Start-End Sensor';

            % Create EditField_StartSensor
            app.EditField_StartSensor = uieditfield(app.ManoMapUIFigure, 'numeric');
            app.EditField_StartSensor.ValueChangedFcn = createCallbackFcn(app, @EditField_StartSensorValueChanged, true);
            app.EditField_StartSensor.Position = [121 88 38 29];

            % Create EditField_EndSensor
            app.EditField_EndSensor = uieditfield(app.ManoMapUIFigure, 'numeric');
            app.EditField_EndSensor.ValueChangedFcn = createCallbackFcn(app, @EditField_EndSensorValueChanged, true);
            app.EditField_EndSensor.Position = [175 89 38 29];

            % Create AddEventFieldTimeLabel
            app.AddEventFieldTimeLabel = uilabel(app.ManoMapUIFigure);
            app.AddEventFieldTimeLabel.HorizontalAlignment = 'right';
            app.AddEventFieldTimeLabel.Position = [400 100 100 22];
            app.AddEventFieldTimeLabel.Text = 'Time';

            % Create AddEventTimeField
            app.AddEventTimeField = uieditfield(app.ManoMapUIFigure, 'numeric');
            app.AddEventTimeField.HorizontalAlignment = 'right';
            app.AddEventTimeField.Position = [400 75 100 22];

            % Create AddEventFieldNameLabel
            app.AddEventFieldNameLabel = uilabel(app.ManoMapUIFigure);
            app.AddEventFieldNameLabel.HorizontalAlignment = 'right';
            app.AddEventFieldNameLabel.Position = [400 55 100 22];
            app.AddEventFieldNameLabel.Text = 'Event Name';

            % Create AddEventNameField
            app.AddEventNameField = uieditfield(app.ManoMapUIFigure);
            app.AddEventNameField.HorizontalAlignment = 'right';
            app.AddEventNameField.Position = [400 35 100 22];

            % Create AddEventButton
            app.AddEventButton = uibutton(app.ManoMapUIFigure, 'push');
            app.AddEventButton.ButtonPushedFcn = createCallbackFcn(app, @AddEventButtonPushed, true);
            app.AddEventButton.BackgroundColor = [0.902 0.902 0.902];
            app.AddEventButton.FontColor = [0.149 0.149 0.149];
            app.AddEventButton.Position = [400 10 100 22];
            app.AddEventButton.Text = 'Add Event';


            % Show the figure after all components are created
            app.ManoMapUIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = manoMap
            
            if datetime > '01-Jan-2042 12:00:00'
                fprintf('Self Destructed App after 01-Jan-2028')
                return 
            else 

            % Create UIFigure and components
            createComponents(app)
            
            end
            
            % Register the app with App Designer
            registerApp(app, app.ManoMapUIFigure)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.ManoMapUIFigure)
        end
    end
end