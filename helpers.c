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
    int redSum = 0, greenSum = 0, blueSum = 0, pixels = 0;
    RGBTRIPLE pxl;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            for (int k = i - 1; k <= i + 1; k++)
            {
                for (int l = j - 1; l <= j + 1; l++)
                {
                    if (k >= 0 && k < width - 1 && l >= 0 && l < height - 1)
                    {
                        pxl = image[k][l];
                        redSum += pxl.rgbtRed;
                        greenSum += pxl.rgbtGreen;
                        blueSum += pxl.rgbtBlue;
                        pixels++;
                    }
                }
            }
            pxl = image[i][j];
            pxl.rgbtRed = redSum / pixels;
            pxl.rgbtGreen = greenSum / pixels;
            pxl.rgbtBlue = blueSum / pixels;
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
