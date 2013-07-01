% @brief Moskowitz like questionariee generator
% @input nElpS = [6,6,6,6,6,6]; %[6,6,6,6,6,6]; % Num of vingettes
% @input nV Num of vingettes
% @input nElpV Nummber of elements per vignetes
% @input nElApps Number of appearances of elemnts in a questionariee
% @return indMat A matrix of selected indeces
% @return nVgen Number of generated vignettes
%
% @author Andrej Košir

function [indMat, nVgen] = generateVignetes(nElpS, nV, nElpV, nElApps)

    % Get basic pars
    nS = numel(nElpS); % Num of siloses 
    nE = sum(nElpS); % Num of elts
    nVgen = nV;

    % Incidence matrix computation
    indMat = zeros(nE, nV); % Incidence matrix
    inSilInds = zeros(nElpV, 1); % Indeces of elements in siloes
    maxEls = max(nElpS);

    numOfApps = zeros(nS, maxEls); % store number of appearances
    leftEltInds = zeros(nS, maxEls+1); % which index is still left. One line for each silos
    leftSiloInds = zeros(nS+1, 1);
    % indsLeft, ind1, ind2, ...
    % indsLeft, ind1, ind2, ...
    % .....
    curEltInds = zeros(nElpV, 1); % to store 1D inds of elts

    % Initialize indices in leftEltInds
    for (ii=1:nS)
        leftEltInds(ii, 1) = nElpS(ii);
        leftEltInds(ii, 2:nElpS(ii)+1) = 1:nElpS(ii);
    end

    % Initialize leftSiloInds
    leftSiloInds(1) = nS;
    leftSiloInds(2:end) = 1:nS;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    for (jj=1:nV) % For each vignette
        currnS = leftSiloInds(1); % If we are out of elts, exit
        if (currnS<4)
            nVgen = jj-1;
            return;
        end
        currPer = randperm(currnS);
        currCutPer = currPer(1:nElpV)';
        currS = leftSiloInds(currCutPer+1); % Select siloses;
        for (kk=1:nElpV)
            % Get ind of elt in a silos
            cP = randperm(leftEltInds(currS(kk), 1)); % Select from what is left
            inSilInds(kk)= leftEltInds(currS(kk), cP(1)+1);

            % Add to num of appearences
            numOfApps(currS(kk), inSilInds(kk)) = numOfApps(currS(kk), inSilInds(kk)) + 1;
        end

        % Set selections
        for (kk=1:nElpV) % Compute 1D indices of elts
            curEltInds(kk) = sum(nElpS(1:(currS(kk)-1))) + inSilInds(kk);
        end
        indMat(curEltInds, jj) = 1;

        % Update leftEltInds - what has remained from elements
        for (kk=1:nElpV) 
            sInd = currS(kk);
            eInd = inSilInds(kk);
            if (numOfApps(sInd, eInd) == nElApps) % Remove elemnt from available elts list
                leftEltInds(sInd, 1) = leftEltInds(sInd, 1) - 1; % Reduce number of all apps
                indToRemove = find(numOfApps(sInd, :) == nElApps);
                posToRemove = find(leftEltInds(sInd, 2:end) == indToRemove)+1;
                leftEltInds(sInd, posToRemove:end-1) = leftEltInds(sInd, posToRemove+1:end);
                leftEltInds(sInd, end) = -1;
                numOfApps(sInd, eInd) = -1; % To prevent next indication

                if (leftEltInds(sInd, 1) == 0) % Remove silos from available siloes list
                    leftSiloInds(1) = leftSiloInds(1) - 1;
                    indToRemove = find(leftSiloInds(2:end) == sInd);
                    leftSiloInds(indToRemove+1:end-1) = leftSiloInds(indToRemove+2:end);
                    leftSiloInds(end) = -1;
                end
            end

        end


    end

end