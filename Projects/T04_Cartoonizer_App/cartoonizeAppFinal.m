function cartoonizeAppFinal()
    % Main Box
    fig = uifigure('Name', 'Cartoonizer', 'Position', [100, 100, 650, 450]);

    % User Interface (UI) Components
    btnLoad = uibutton(fig, 'push', 'Text', 'Upload Image', 'Position', [10, 400, 100, 30], 'ButtonPushedFcn', @(btnLoad, event) loadImage());
    btnCartoonize = uibutton(fig, 'push', 'Text', 'Cartoonize', 'Position', [120, 400, 100, 30], 'ButtonPushedFcn', @(btnCartoonize, event) cartoonizeImage());

    % Slider for Edge Thickness
    lblEdgeSize = uilabel(fig, 'Position', [240, 400, 100, 30], 'Text', 'Edge Size:');
    sldEdgeSize = uislider(fig, 'Position', [310, 410, 150, 3], 'Limits', [1, 5], 'Value', 1, 'MajorTicks', [1, 2, 3, 4, 5]);

    % Dropdown for Color Quantization
    lblColors = uilabel(fig, 'Position', [480, 400, 150, 30], 'Text', 'Color Quantization:');
    ddColors = uidropdown(fig, 'Position', [600, 405, 50, 30], 'Items', {'8', '16', '32', '64'}, 'Value', '16');

    % Axes for Display
    axOriginal = uiaxes(fig, 'Position', [10, 50, 300, 300]);
    axOriginal.Title.String = 'Original Image';
    axCartoon = uiaxes(fig, 'Position', [330, 50, 300, 300]);
    axCartoon.Title.String = 'Cartoonized Image';

    % Variables to Store Images
    originalImage = [];

    function loadImage()
        % Load Image
        [file, path] = uigetfile({'*.jpg;*.png;*.jpeg'}, 'Select an Image');
        if isequal(file, 0)
            return;
        end
        try
            % Different file formats
            [~, ~, ext] = fileparts(file);
            validExtensions = {'.jpg', '.png', '.jpeg'};
            if ~ismember(lower(ext), validExtensions)
                error('Invalid file format.');
            end
            originalImage = imread(fullfile(path, file));
            imshow(originalImage, 'Parent', axOriginal);
        catch ME
            uialert(fig, 'Invalid image format or file.', 'Error');
        end
    end

    function cartoonizeImage()
        if isempty(originalImage)
            uialert(fig, 'Please upload an image first.', 'No Image');
            return;
        end

        % Retrieve User Selected Parameters such as from Slider or Dropdown
        edgeSize = round(sldEdgeSize.Value); % Edge thickness from slider
        numColors = str2double(ddColors.Value); % Number of colors from dropdown

        % Step 1: Convert to grayscale
        grayImage = rgb2gray(originalImage);

        % Step 2: Apply Gaussian smoothing to reduce noise
        smoothedImage = imgaussfilt(grayImage, 2);

        % Step 3: Edge Detection (Canny)
        edges = edge(smoothedImage, 'Canny', [0.1 0.3]); % Thresholds adjusted to minimize unnecessary edges

        % Step 4: Dilate edges to enhance cartoon effect
        edges = imdilate(edges, strel('disk', edgeSize));

        % Step 5: Color Quantization
        %Reduces the number of distinct colors in the image to numColors
        [quantizedImage, colormap] = rgb2ind(originalImage, numColors);
        quantizedImage = ind2rgb(quantizedImage, colormap);

        % Step 6: Combine Edges and Colors
        edges3D = repmat(edges, [1, 1, 3]); % Match RGB dimensions / Convert 2D edge map into a 3D binary Mask
        cartoonImage = imbilatfilt(quantizedImage); % Apply bilateral filtering for smoother effect
        cartoonImage(edges3D) = 0; % Set edge pixels to black

        % Display Result
        imshow(cartoonImage, 'Parent', axCartoon);
    end
end
