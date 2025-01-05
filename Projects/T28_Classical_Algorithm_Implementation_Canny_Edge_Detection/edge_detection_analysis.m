function edge_detection_analysis()
    % Dataset path
    folder = '/MATLAB Drive/SUJANADIP/natural_images';
    output_pdf_path = '/MATLAB Drive/SUJANADIP/edge_detection_analysis_report.pdf';
    output_image_path = '/MATLAB Drive/SUJANADIP/edge_detection_results.png';
    num_images = 5; % Number of images to showcase

    % Ensure the folder exists
    if ~isfolder(folder)
        error('The specified folder does not exist: %s', folder);
    end

    % Get all image files recursively
    files = get_all_images_recursive(folder);

    % Check if valid images exist
    if isempty(files)
        error('No image files found in the folder or subfolders: %s', folder);
    end

    % Showcase results for a subset of images
    fprintf('\nShowcasing Results for a Subset of Images:\n');
    showcase_results_with_metrics(files, num_images, output_image_path);

    % Summarize metrics for the entire dataset
    fprintf('\nSummarizing Metrics for the Entire Dataset:\n');
    summarize_dataset_metrics(files);

    % Save results as a PDF
    fprintf('\nSaving Results as a PDF Report:\n');
    save_results_as_pdf(files, output_pdf_path, num_images);

    fprintf('\nResults saved to:\nPDF: %s\nImage: %s\n', output_pdf_path, output_image_path);
end

function files = get_all_images_recursive(folder)
    % Recursively get all image files from folder and subfolders
    file_types = {'*.png', '*.jpg', '*.jpeg', '*.bmp'};
    files = [];
    for i = 1:length(file_types)
        files = [files; dir(fullfile(folder, '**', file_types{i}))];
    end
end

function [edge_density, mean_gradient_magnitude] = evaluate_edge_detection(image_path, edges)
    % Read the original image
    original = imread(image_path);
    if size(original, 3) == 3
        original = rgb2gray(original);
    end

    % Edge Pixel Density
    edge_density = sum(edges(:) > 0) / numel(edges);

    % Mean Gradient Magnitude
    [grad_x, grad_y] = imgradientxy(original, 'sobel');
    gradient_magnitude = sqrt(grad_x.^2 + grad_y.^2);
    mean_gradient_magnitude = mean(gradient_magnitude(:));
end

function showcase_results_with_metrics(files, num_images, output_image_path)
    fprintf('%-40s %-15s %-20s\n', 'Image Name', 'Edge Density', 'Mean Gradient Magnitude');
    fprintf('%s\n', repmat('-', 1, 80));

    num_files = min(num_images, length(files));
    rows = num_files; % Number of rows for the output image
    figure;

    for idx = 1:num_files
        filename = files(idx).name;
        image_path = fullfile(files(idx).folder, filename);
        image = imread(image_path);
        if size(image, 3) == 3
            image = rgb2gray(image);
        end

        % Canny Edge Detection
        edges = edge(image, 'Canny');

        % Calculate Metrics
        [edge_density, mean_grad_mag] = evaluate_edge_detection(image_path, edges);
        fprintf('%-40s %-15.4f %-20.4f\n', filename, edge_density, mean_grad_mag);

        % Plot Original and Edges
        subplot(rows, 2, 2 * (idx - 1) + 1);
        imshow(image);
        title(['Original: ', filename], 'Interpreter', 'none');

        subplot(rows, 2, 2 * (idx - 1) + 2);
        imshow(edges);
        title(['Edges: ', filename], 'Interpreter', 'none');
    end

    % Save results as an image
    saveas(gcf, output_image_path);
    close(gcf);
end

function summarize_dataset_metrics(files)
    total_images = length(files);
    total_edge_density = 0;
    total_grad_mag = 0;

    for idx = 1:total_images
        image_path = fullfile(files(idx).folder, files(idx).name);
        image = imread(image_path);
        if size(image, 3) == 3
            image = rgb2gray(image);
        end

        edges = edge(image, 'Canny');
        [edge_density, mean_grad_mag] = evaluate_edge_detection(image_path, edges);

        total_edge_density = total_edge_density + edge_density;
        total_grad_mag = total_grad_mag + mean_grad_mag;
    end

    % Calculate and Print Summary
    avg_edge_density = total_edge_density / total_images;
    avg_grad_mag = total_grad_mag / total_images;
    fprintf('Total Images Processed: %d\n', total_images);
    fprintf('Average Edge Density: %.4f\n', avg_edge_density);
    fprintf('Average Gradient Magnitude: %.4f\n', avg_grad_mag);
end

function save_results_as_pdf(files, pdf_path, num_images)
    % Initialize PDF
    import mlreportgen.dom.*;
    doc = Document(pdf_path, 'pdf');

    num_files = min(num_images, length(files));

    for idx = 1:num_files
        filename = files(idx).name;
        image_path = fullfile(files(idx).folder, filename);
        image = imread(image_path);
        if size(image, 3) == 3
            image = rgb2gray(image);
        end

        edges = edge(image, 'Canny');

        % Create Figures
        figure;
        subplot(1, 2, 1);
        imshow(image);
        title(['Original: ', filename], 'Interpreter', 'none');

        subplot(1, 2, 2);
        imshow(edges);
        title(['Edges: ', filename], 'Interpreter', 'none');

        % Save to Temporary File
        temp_image_path = fullfile(tempdir, ['temp_', num2str(idx), '.png']);
        saveas(gcf, temp_image_path);

        % Add to PDF
        img = Image(temp_image_path);
        append(doc, img);

        % Close figure
        close(gcf);
    end

    close(doc);
end
