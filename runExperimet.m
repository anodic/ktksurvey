% runExperimet

% Notes:
%  - we must have: numOfSiloses > numOfEltsPerVig

nElpS = [6,6,6,6,6,6]; %[6,6,6,6,6,6]; % Num of vingettes
nV = 48; % Num of vingettes
nElpV = 4; % Num of elements per vignetes
nElApps = 5; % umber of appearances of 

[indMat, nVgen] = generateVignetes(nElpS, nV, nElpV, nElApps);





%% Test it
% Equal of siloses
%sum(indMat, 2)

% equal of elements
%sum(indMat)


% Loop
n = 1000;
nVLst = zeros(1, n);
minEltsUsed = zeros(1, n);
for (nn=1:n)
    [indMat, nVgen] = generateVignetes(nElpS, nV, nElpV, nElApps);
    nVLst(nn) = nVgen;
    minEltsUsed(nn) = min(sum(indMat, 2));
end


figure(1);
plot(nVLst, 'b'); 
title('Number of gen vignetes');
figure(2);
plot(minEltsUsed, 'r');
title('Min number of used elts');
