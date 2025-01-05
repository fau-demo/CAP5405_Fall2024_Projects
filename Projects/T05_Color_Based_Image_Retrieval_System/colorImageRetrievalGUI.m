function colorImageRetrievalGUI()
    % Create the main GUI figure
    fig = uifigure('Name', 'Color-Based Image Retrieval', 'Position', [100, 100, 1000, 700]);
    
    % Create buttons and labels
    loadButton = uibutton(fig, 'push', 'Text', 'Load Dataset', ...
                          'Position', [50, 600, 150, 30], ...
                          'ButtonPushedFcn', @(btn, event) loadDataset(fig));
    selectButton = uibutton(fig, 'push', 'Text', 'Select Query Image', ...
                            'Position', [250, 600, 150, 30], ...
                            'Enable', 'off', ...
                            'ButtonPushedFcn', @(btn, event) selectQueryImage(fig));
    resultPanel = uipanel(fig, 'Title', 'Results', 'Position', [50, 50, 900, 500]);
    resultsAxes = gobjects(1, 6);
    resultsAxesHist = gobjects(1, 6);
    
    % Create axes for images and histograms
    for i = 1:6
        resultsAxes(i) = uiaxes(resultPanel, 'Position', [30 + (i - 1) * 150, 300, 130, 130]);
        resultsAxesHist(i) = uiaxes(resultPanel, 'Position', [30 + (i - 1) * 150, 100, 130, 130]);
        if i == 1
            title(resultsAxes(i), 'Query Image');
            title(resultsAxesHist(i), 'Query Histogram');
        else
            title(resultsAxes(i), sprintf('Match %d', i - 1));
            title(resultsAxesHist(i), sprintf('Histogram %d', i - 1));
        end
    end
    
    % Initialize global variables for dataset and results
    global imageFiles histograms averageRGBValues numImages;
    histograms = [];
    averageRGBValues = [];
    
    % Function to load dataset
    function loadDataset(fig)
        datasetPath = uigetdir(pwd, 'Select Dataset Folder');
        if datasetPath == 0
            uialert(fig, 'No folder selected!', 'Error');
            return;
        end
        
        imageFiles = dir(fullfile(datasetPath, '**', '*.jpg')); % Adjust for other formats if needed
        numImages = length(imageFiles);
        
        % Initialize storage for histograms and RGB values
        histograms = zeros(numImages, 256 * 3);
        averageRGBValues = zeros(numImages, 3);
        
        % Process images
        disp('Processing dataset...');
        for i = 1:numImages
            imgPath = fullfile(imageFiles(i).folder, imageFiles(i).name);
            img = imread(imgPath);
            img = imresize(img, [224 224]); % Resize for consistency
            
            % Calculate histograms
            rHist = imhist(img(:, :, 1), 256);
            gHist = imhist(img(:, :, 2), 256);
            bHist = imhist(img(:, :, 3), 256);
            
            % Normalize and store histograms
            histograms(i, :) = [rHist / sum(rHist); gHist / sum(gHist); bHist / sum(bHist)]';
            
            % Calculate average RGB values
            averageRGBValues(i, :) = mean(reshape(img, [], 3));
        end
        
        disp('Dataset loaded successfully!');
        selectButton.Enable = 'on';
        uialert(fig, 'Dataset loaded successfully!', 'Success');
    end
    
    % Function to select query image
    function selectQueryImage(fig)
        [filename, pathname] = uigetfile({'*.jpg;*.png;*.jpeg;*.tiff', 'Image Files (*.jpg, *.png, *.jpeg, *.tiff)'}, 'Select Query Image');
        if isequal(filename, 0)
            uialert(fig, 'No file selected!', 'Error');
            return;
        end
        
        queryImgPath = fullfile(pathname, filename);
        queryImg = imread(queryImgPath);
        queryImg = imresize(queryImg, [224 224]); % Resize to match dataset images
        
        % Calculate query image histogram
        rHistQuery = imhist(queryImg(:, :, 1), 256);
        gHistQuery = imhist(queryImg(:, :, 2), 256);
        bHistQuery = imhist(queryImg(:, :, 3), 256);
        queryHistogram = [rHistQuery / sum(rHistQuery); gHistQuery / sum(gHistQuery); bHistQuery / sum(bHistQuery)]';
        
        % Calculate average RGB values for the query image
        queryAvgRGB = mean(reshape(queryImg, [], 3));
        
        % Compare with dataset histograms
        distances = zeros(numImages, 1);
        for i = 1:numImages
            distances(i) = norm(histograms(i, :) - queryHistogram);
        end
        
        % Sort and find top matches
        [~, sortedIndices] = sort(distances);
        topN = 5;
        topMatches = sortedIndices(1:topN);
        
        % Update GUI with results
        imshow(queryImg, 'Parent', resultsAxes(1));
        title(resultsAxes(1), sprintf('Query\nRGB: [%d, %d, %d]', round(queryAvgRGB)));
        bar(resultsAxesHist(1), 1:256, [rHistQuery, gHistQuery, bHistQuery]);
        legend(resultsAxesHist(1), {'Red', 'Green', 'Blue'});
        
        for i = 1:topN
            matchImgPath = fullfile(imageFiles(topMatches(i)).folder, imageFiles(topMatches(i)).name);
            matchImg = imread(matchImgPath);
            matchAvgRGB = averageRGBValues(topMatches(i), :);
            
            % Show image
            imshow(matchImg, 'Parent', resultsAxes(i + 1));
            title(resultsAxes(i + 1), sprintf('Match %d\nRGB: [%d, %d, %d]', i, round(matchAvgRGB)));
            
            % Show histogram
            rHistMatch = imhist(matchImg(:, :, 1), 256);
            gHistMatch = imhist(matchImg(:, :, 2), 256);
            bHistMatch = imhist(matchImg(:, :, 3), 256);
            bar(resultsAxesHist(i + 1), 1:256, [rHistMatch / sum(rHistMatch), gHistMatch / sum(gHistMatch), bHistMatch / sum(bHistMatch)]);
            legend(resultsAxesHist(i + 1), {'Red', 'Green', 'Blue'});
        end
    end
end
