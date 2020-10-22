#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float avg = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE pxl = image[i][j];
            avg = (pxl.rgbtRed + pxl.rgbtGreen + pxl.rgbtBlue) / 3.0;
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = roundf(avg);
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE reversed[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            reversed[i][width - j - 1] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = reversed[i][j];
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blurred[height][width];
    RGBTRIPLE pxl;
    float redSum = 0, greenSum = 0, blueSum = 0, pixels = 0;
    for (int i = 0; i < height; i++) // Search on each row
    {
        for (int j = 0; j < width; j++) // Search on each spot of row (column)
        {
            for (int k = i - 1; k <= i + 1; k++) // Sums RGB valuez within 3 rowas
            {
                for (int l = j - 1; l <= j + 1; l++) //Sums RGB valuez within 3 columns
                {
                    if (k >= 0 && k < height && l >= 0 && l < width) // Only sum if it is insdide the image frame. This is for edges andcorners.
                    {
                        pxl = image[k][l];
                        redSum += pxl.rgbtRed;
                        greenSum += pxl.rgbtGreen;
                        blueSum += pxl.rgbtBlue;
                        pixels++;
                    }
                }
            }
            blurred[i][j].rgbtRed = round(redSum / pixels);
            blurred[i][j].rgbtGreen = round(greenSum / pixels);
            blurred[i][j].rgbtBlue = round(blueSum / pixels);
            redSum = greenSum = blueSum = pixels = 0;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blurred[i][j];
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE edged[height][width];
    RGBTRIPLE pxl;
    float Gx[3][3] = {{-1.0, 0.0, 1.0}, {-2.0, 0.0, 2.0}, {-1.0, 0.0, 1.0}}; // Array for Gx
    float Gy[3][3] = {{-1.0, -2.0, -1.0}, {0.0, 0.0, 0.0}, {1.0, 2.0, 1.0}}; // Array for Gy
    float redSumGx = 0.0, greenSumGx = 0.0, blueSumGx = 0.0; // Gx for each channel
    float redSumGy = 0.0, greenSumGy = 0.0, blueSumGy = 0.0; // Gy for each channel
    float redSumOpt = 0.0, greenSumOpt = 0.0, blueSumOpt = 0.0; // Output for each channel
    for (int i = 0; i < height; i++) // Search on each row
    {
        for (int j = 0; j < width; j++) // Search on each spot of row (column)
        {
            for (int k = i - 1, x = 0; k <= i + 1; k++, x++) // Loops within 3 rowas
            {
                for (int l = j - 1, y = 0; l <= j + 1; l++, y++) //Loops within 3 columns
                {
                    if (k >= 0 && k < height && l >= 0 && l < width) // Check if it is insdide the image frame. This is for edges andcorners.
                    {
                        pxl = image[k][l];

                        redSumGx += pxl.rgbtRed * Gx[x][y];
                        greenSumGx += pxl.rgbtGreen * Gx[x][y];
                        blueSumGx += pxl.rgbtBlue * Gx[x][y];

                        redSumGy += pxl.rgbtRed * Gy[x][y];
                        greenSumGy += pxl.rgbtGreen * Gy[x][y];
                        blueSumGy += pxl.rgbtBlue * Gy[x][y];
                    }
                }
            }
            redSumOpt = roundf(sqrt((redSumGx * redSumGx) + (redSumGy * redSumGy)));
            greenSumOpt = roundf(sqrt((greenSumGx * greenSumGx) + (greenSumGy * greenSumGy)));
            blueSumOpt = roundf(sqrt((blueSumGx * blueSumGx) + (blueSumGy * blueSumGy)));
            edged[i][j].rgbtRed = redSumOpt < 255 ? redSumOpt : 255;
            edged[i][j].rgbtGreen = greenSumOpt < 255 ? greenSumOpt : 255;
            edged[i][j].rgbtBlue = blueSumOpt < 255 ? blueSumOpt : 255;
            redSumGx = greenSumGx = blueSumGx = 0.0;
            redSumGy = greenSumGy = blueSumGy = 0.0;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = edged[i][j];
        }
    }
}
