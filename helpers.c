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
    float redSum = 0, greenSum = 0, blueSum = 0, pixels = 0;
    RGBTRIPLE pxl;
    for (int i = 0; i < height; i++) // Search on each row
    {
        for (int j = 0; j < width; j++) // Search on each spot of row (column)
        {
            for (int k = i - 1; k <= i + 1; k++) //
            {
                for (int l = j - 1; l <= j + 1; l++)
                {
                    if (k >= 0 && k < height && l >= 0 && l < width)
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
    return;
}
