function [clst,imageSinglePoint] = getChanIdxFrmt(x,A,pixList)

imageSinglePoint = zeros(size(x));

%convert binary pixel list to channel and index number
%choosing the center fiducial marker in the channel 

clst={};n=1;
sz=[size(x)];

for i = 1:length(pixList)
%     keyboard
    %
%     [r, c] = find(A==i); 
    [r,c] = ind2sub(sz,pixList{i});

%     [newR,I] = sort(r); % could do without
%     newC=c(I);
    chans = unique(r);
    
    if length(chans)>=4 % requires 4 or more channels to group
    
        for  j = 1:length(chans)%loop through all chans 
%             [xx]=find(r==chans(j));
            xx=r==chans(j);
            colsIndx = c(xx);
            midPointIndx = round(length(colsIndx)/2);
            
            clst{n}(j,1)=chans(j);
            clst{n}(j,2)=colsIndx(midPointIndx);
            imageSinglePoint(chans(j),colsIndx(midPointIndx))=1;
        end
        n=n+1;
    end
end

% keyboard
end


%  function idx = myFind( x )
%      allIdx = 1:numel(x) ;
%      idx = allIdx(x ~= 0) ;
%  end