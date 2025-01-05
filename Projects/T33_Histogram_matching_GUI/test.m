function test
    % Create a figure and UI elements
    % Create the main figure window for the application with custom settings
    f = figure('Name', 'Advanced Freehand Drawing with Histogram Matching', ...
               'NumberTitle', 'off', 'MenuBar', 'none', 'ToolBar', 'none', ...
               'Color', [0.9, 0.9, 0.9], 'Position', [100, 100, 1000, 600]);

    % Create axes for drawing
    % Create an axes object within the figure to act as the drawing canvas
    ax = axes('Parent', f, 'Position', [0.05, 0.2, 0.6, 0.75]);
    % Display a blank white image on the canvas
    imshow(ones(512, 512), 'Parent', ax);
    hold on; % Allow multiple graphical objects to be drawn on the canvas

    % Variables to store the drawn image and brush size
    freehandMask = ones(512, 512); % Binary mask for the freehand drawing
    drawnImage = []; % Variable to store the current drawing
    brushColor = [0, 0, 0]; % Default brush color (black)
    brushSize = 5; % Default brush size

    % UI elements for features
    % Button to start drawing
    uicontrol('Style', 'pushbutton', 'String', 'Draw', 'Position', [20, 20, 100, 30], ...
              'Callback', @startDrawing);
    % Button to match histogram with a reference image
    uicontrol('Style', 'pushbutton', 'String', 'Match Histogram', 'Position', [140, 20, 150, 30], ...
              'Callback', @matchHistogram);
    % Button to undo the last drawing action
    uicontrol('Style', 'pushbutton', 'String', 'Undo', 'Position', [320, 20, 100, 30], ...
              'Callback', @undoDrawing);
    % Button to reset the canvas to blank
    uicontrol('Style', 'pushbutton', 'String', 'Reset', 'Position', [440, 20, 100, 30], ...
              'Callback', @resetCanvas);
    % Button to save the current drawing to a file
    uicontrol('Style', 'pushbutton', 'String', 'Save Drawing', 'Position', [560, 20, 120, 30], ...
              'Callback', @saveDrawing);
    % Button to load a saved drawing from a file
    uicontrol('Style', 'pushbutton', 'String', 'Load Drawing', 'Position', [700, 20, 120, 30], ...
              'Callback', @loadDrawing);
    % Label for the brush size slider
    uicontrol('Style', 'text', 'String', 'Brush Size:', 'Position', [850, 20, 70, 20]);
    % Slider to adjust the brush size dynamically
    brushSlider = uicontrol('Style', 'slider', 'Min', 1, 'Max', 20, 'Value', brushSize, ...
                            'Position', [920, 20, 50, 20], 'Callback', @adjustBrushSize);
    % Label for the brush color picker
    uicontrol('Style', 'text', 'String', 'Brush Color:', 'Position', [850, 50, 70, 20]);
    % Button to select the brush color
    uicontrol('Style', 'pushbutton', 'String', 'Select Color', 'Position', [920, 50, 100, 30], ...
              'Callback', @selectColor);

    % Stack to store drawing history for undo functionality
    drawingHistory = {}; % Cell array to store previous states of the drawing

    % Function to start freehand drawing
    function startDrawing(~, ~)
        % Allow freehand drawing with the selected brush size and color
        h = drawfreehand('LineWidth', brushSize, 'Color', brushColor);

        % Create a binary mask from the drawing
        freehandMask = createMask(h);
        
        % Initialize drawnImage if it's empty
        if isempty(drawnImage)
            drawnImage = ones(512, 512) * 255; % Start with a blank canvas
        end
        
        % Apply the mask to the drawn image
        drawnImage(freehandMask) = randi([0, 255], sum(freehandMask(:)), 1);
        drawingHistory{end + 1} = drawnImage; % Save the current state to history
        imshow(drawnImage, 'Parent', ax); % Update the canvas
    end

    % Function to match the histogram of the drawn image with a reference image
    function matchHistogram(~, ~)
        % Check if there's a drawing to match
        if isempty(drawnImage)
            msgbox('Please draw something first!', 'Error', 'error'); % Error message
            return;
        end

        % Open a file selection dialog for the reference image
        [file, path] = uigetfile({'*.jpg;*.png;*.bmp', 'Image Files (*.jpg, *.png, *.bmp)'});
        if isequal(file, 0)
            return; % Exit if the user cancels
        end
        refImage = imread(fullfile(path, file)); % Load the reference image
        refImage = imresize(rgb2gray(refImage), [512, 512]); % Resize and convert to grayscale

        % Perform histogram matching
        matchedImage = imhistmatch(drawnImage, refImage);

        % Display the matched image in a new figure
        figure('Name', 'Histogram Matched Image', 'NumberTitle', 'off');
        imshow(matchedImage);
    end

    % Function to undo the last drawing
    function undoDrawing(~, ~)
        % Check if there's a history to undo
        if ~isempty(drawingHistory)
            drawingHistory(end) = []; % Remove the last state
            if isempty(drawingHistory)
                drawnImage = ones(512, 512) * 255; % Reset to blank canvas
            else
                drawnImage = drawingHistory{end}; % Restore the last saved state
            end
            imshow(drawnImage, 'Parent', ax); % Update the canvas
        else
            msgbox('Nothing to undo!', 'Error', 'error'); % Error message
        end
    end

    % Function to reset the canvas
    function resetCanvas(~, ~)
        drawnImage = ones(512, 512) * 255; % Reset to blank canvas
        drawingHistory = {}; % Clear history
        imshow(drawnImage, 'Parent', ax); % Update the canvas
    end

    % Function to save the drawing
    function saveDrawing(~, ~)
        % Open a file selection dialog for saving the drawing
        [file, path] = uiputfile({'*.png', 'PNG Image (*.png)'; '*.jpg', 'JPEG Image (*.jpg)'});
        if isequal(file, 0)
            return; % Exit if the user cancels
        end
        imwrite(uint8(drawnImage), fullfile(path, file)); % Save the drawing as an image file
    end

    % Function to load a saved drawing
    function loadDrawing(~, ~)
        % Open a file selection dialog to load a saved drawing
        [file, path] = uigetfile({'*.png;*.jpg', 'Image Files (*.png, *.jpg)'});
        if isequal(file, 0)
            return; % Exit if the user cancels
        end
        loadedImage = imread(fullfile(path, file)); % Load the image
        drawnImage = imresize(rgb2gray(loadedImage), [512, 512]); % Resize and convert to grayscale
        drawingHistory = {drawnImage}; % Initialize history with the loaded image
        imshow(drawnImage, 'Parent', ax); % Update the canvas
    end

    % Function to adjust brush size
    function adjustBrushSize(~, ~)
        % Update the brush size based on the slider value
        brushSize = round(get(brushSlider, 'Value'));
    end

    % Function to select brush color
    function selectColor(~, ~)
        % Open a color selection dialog for the brush
        brushColor = uisetcolor(brushColor, 'Select Brush Color');
    end
end
