% Color-Based Image Retrieval GUI
% Author: Naga Prem Sai Nellure
% Date: December 7, 2024
%
% Description:
% This MATLAB GUI application implements a color-based image retrieval system.
% It uses RGB histogram comparisons to find the most similar images to a query
% image from a given dataset. The application supports dataset loading, query
% image selection, and result visualization.
%
% References:
% 1. MATLAB Documentation: MATLAB Image Processing Toolbox 
%    https://www.mathworks.com/help/images/
%
% 2. RGB Histogram Techniques:
%    - Understanding Histogram Comparison for Image Similarity
%      https://www.sciencedirect.com/science/article/pii/S003132031730340X
%    - YouTube Video: "Image Histograms for Computer Vision"
%      https://www.youtube.com/watch?v=4bf0iO4lxuo&t=62s
%
% 3. Histogram-Based Image Retrieval Techniques:
%    - Research Paper: "Histogram-Based Image Retrieval"
%      DOI: 10.1109/ITNG.2009.126
%    - YouTube Video: "Basics of Histogram Comparison"
%      https://www.youtube.com/watch?v=leLcNHKAFEY
%
% 4. GUI Implementation in MATLAB:
%    - YouTube Video: "Creating MATLAB GUIs with App Designer"
%      https://www.youtube.com/watch?v=MUySM16gbGA
%
% Usage:
% Run this script in MATLAB. Requires the Image Processing Toolbox.

function colorImageRetrievalGUI()
    % Create the main GUI figure
    fig = uifigure('Name', 'Color-Based Image Retrieval', 'Position', [100, 100, 1000, 800]);
    
    % Create buttons
    loadButton = uibutton(fig, 'push', 'Text', 'Load Dataset', ...
                          'Position', [50, 700, 150, 30], ...
                          'ButtonPushedFcn', @(btn, event) loadDataset(fig));
    selectButton = uibutton(fig, 'push', 'Text', 'Select Query Image', ...
                            'Position', [250, 700, 150, 30], ...
                            'Enable', 'off', ...
                            'ButtonPushedFcn', @(btn, event) selectQueryImage(fig));
    clearButton = uibutton(fig, 'push', 'Text', 'Clear Images', ...
                           'Position', [450, 700, 150, 30], ...
                           'Enable', 'off', ...
                           'ButtonPushedFcn', @(btn, event) clearImages());

    % Create results panel
    resultPanel = uipanel(fig, 'Title', 'Results', 'Position', [50, 50, 900, 600]);
    resultsAxes = gobjects(1, 6);
    histAxes = gobjects(1, 6);
    
    for i = 1:6
        resultsAxes(i) = uiaxes(resultPanel, 'Position', [30 + (i - 1) * 140, 350, 130, 130]);
        histAxes(i) = uiaxes(resultPanel, 'Position', [30 + (i - 1) * 140, 150, 130, 130]);
        if i == 1
            title(resultsAxes(i), 'Query Image');
            title(histAxes(i), 'Query Histogram');
        else
            title(resultsAxes(i), sprintf('Match %d', i - 1));
            title(histAxes(i), sprintf('Histogram %d', i - 1));
        end
    end
    
    % Initialize global variables
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
        
        % Initialize storage
        histograms = zeros(numImages, 256 * 3);
        averageRGBValues = zeros(numImages, 3);
        
        % Process images
        disp('Processing dataset...');
        for i = 1:numImages
            imgPath = fullfile(imageFiles(i).folder, imageFiles(i).name);
            img = imread(imgPath);
            img = imresize(img, [224 224]);
            
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
        clearButton.Enable = 'on';
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
        queryImg = imresize(queryImg, [224 224]); 
        
        % Calculate query image histogram
        rHistQuery = imhist(queryImg(:, :, 1), 256);
        gHistQuery = imhist(queryImg(:, :, 2), 256);
        bHistQuery = imhist(queryImg(:, :, 3), 256);
        queryHistogram = [rHistQuery / sum(rHistQuery); gHistQuery / sum(gHistQuery); bHistQuery / sum(bHistQuery)]';
        
        % Calculate average RGB values
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
        
        % Display query image and histograms
        imshow(queryImg, 'Parent', resultsAxes(1));
        title(resultsAxes(1), sprintf('Query\nRGB: [%d, %d, %d]', round(queryAvgRGB)));
        bar(histAxes(1), [rHistQuery, gHistQuery, bHistQuery], 'stacked');
        
        % Display matches and histograms
        for i = 1:topN
            matchImgPath = fullfile(imageFiles(topMatches(i)).folder, imageFiles(topMatches(i)).name);
            matchImg = imread(matchImgPath);
            matchAvgRGB = averageRGBValues(topMatches(i), :);
            
            rHist = imhist(matchImg(:, :, 1), 256) / sum(imhist(matchImg(:, :, 1)));
            gHist = imhist(matchImg(:, :, 2), 256) / sum(imhist(matchImg(:, :, 2)));
            bHist = imhist(matchImg(:, :, 3), 256) / sum(imhist(matchImg(:, :, 3)));
            
            imshow(matchImg, 'Parent', resultsAxes(i + 1));
            title(resultsAxes(i + 1), sprintf('Match %d\nRGB: [%d, %d, %d]', i, round(matchAvgRGB)));
            bar(histAxes(i + 1), [rHist, gHist, bHist], 'stacked');
        end
    end

    % Function to clear images and titles
    function clearImages()
        for i = 1:6
            cla(resultsAxes(i)); % Clear image axes
            cla(histAxes(i));    % Clear histogram axes
            if i == 1
                title(resultsAxes(i), 'Query Image'); % Reset title for Query Image
                title(histAxes(i), 'Query Histogram'); % Reset title for Query Histogram
            else
                title(resultsAxes(i), sprintf('Match %d', i - 1)); % Reset title for Match Images
                title(histAxes(i), sprintf('Histogram %d', i - 1)); % Reset title for Match Histograms
            end
        end
    end
end
