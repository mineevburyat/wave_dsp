// bmp.cpp : Defines the entry point for the application.
//

#include "stdafx.h"

void CreateBmp555(char *fname, WORD color);
void CreateBmp24(char *fname, RGBTRIPLE color);
void CreateBmp8(char *fname, BYTE color);
BOOL Convert256To24(char *fin, char *fout);

int APIENTRY WinMain(HINSTANCE hInstance,
					 HINSTANCE hPrevInstance,
					 LPSTR lpCmdLine,
					 int nCmdShow)
{
	WORD color1 = 0x1f02;

	RGBTRIPLE color2;
	color2.rgbtRed = 111;
	color2.rgbtGreen = 20;
	color2.rgbtBlue = 160;

	BYTE color3 = 4;

	CreateBmp555("test1.bmp", color1);
	CreateBmp24("test2.bmp", color2);
	CreateBmp8("test3.bmp", color3);

	Convert256To24("test3.bmp", "test4.bmp");
	return 0;
}

// �������� �������� � ������� bmp 16 ��� ���� 5-5-5, ������� ����� ������ ����������
void CreateBmp555(char *fname, WORD color)
{
	HANDLE hFile;
	DWORD RW;
	int i, j;

	// ������� ������ ���������
	BITMAPFILEHEADER bfh;
	BITMAPINFOHEADER bih;
	BYTE Palette[1024]; // �������

	// ����� � ��� ����� �������� �������� 35 x 50 ��������
	int Width = 33;
	int Height = 50;

	memset(Palette, 0, 1024); // � ������� � ��� ����

	// �������� ��
	memset(&bfh, 0, sizeof(bfh));
	bfh.bfType = 0x4D42;							  // ���������, ��� ��� bmp 'BM'
	bfh.bfOffBits = sizeof(bfh) + sizeof(bih) + 1024; // ������� �������� 1Kb, �� �� ��� ����������� �� �����
	bfh.bfSize = bfh.bfOffBits +
				 sizeof(color) * Width * Height +
				 Height * ((sizeof(color) * Width) % 4); // ��������� ������ ��������� �����

	memset(&bih, 0, sizeof(bih));
	bih.biSize = sizeof(bih);	// ��� ��������
	bih.biBitCount = 16;		// 16 ��� �� �������
	bih.biClrUsed = 32768;		// �� ���������� 5-5-5
	bih.biCompression = BI_RGB; // ��� ������
	bih.biHeight = Height;
	bih.biWidth = Width;
	bih.biPlanes = 1; // ������ ���� 1
					  // � ��������� ���� �������� 0
	hFile = CreateFile(fname, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
	if (hFile == INVALID_HANDLE_VALUE)
		return;

	// ������� ���������
	WriteFile(hFile, &bfh, sizeof(bfh), &RW, NULL);
	WriteFile(hFile, &bih, sizeof(bih), &RW, NULL);

	// ������� �������
	WriteFile(hFile, Palette, 1024, &RW, NULL);
	for (i = 0; i < Height; i++)
	{
		for (j = 0; j < Width; j++)
		{
			WriteFile(hFile, &color, sizeof(color), &RW, NULL);
		}
		// ��������� �� �������
		WriteFile(hFile, Palette, (sizeof(color) * Width) % 4, &RW, NULL);
	}

	CloseHandle(hFile);
}

// �������� �������� � ������� bmp 24 ���
void CreateBmp24(char *fname, RGBTRIPLE color)
{
	HANDLE hFile;
	DWORD RW;
	int i, j;

	// ������� ������ ���������
	BITMAPFILEHEADER bfh;
	BITMAPINFOHEADER bih;
	BYTE Palette[1024]; // �������

	// ����� � ��� ����� �������� �������� 35 x 50 ��������
	int Width = 35;
	int Height = 50;
	memset(Palette, 0, 1024); // � ������� � ��� ����

	// �������� ��
	memset(&bfh, 0, sizeof(bfh));
	bfh.bfType = 0x4D42;							  // ���������, ��� ��� bmp 'BM'
	bfh.bfOffBits = sizeof(bfh) + sizeof(bih) + 1024; // ������� �������� 1Kb, �� �� ��� ����������� �� �����
	bfh.bfSize = bfh.bfOffBits +
				 sizeof(color) * Width * Height +
				 Height * (Width % 4); // ��������� ������ ��������� �����

	memset(&bih, 0, sizeof(bih));
	bih.biSize = sizeof(bih);	// ��� ��������
	bih.biBitCount = 24;		// 16 ��� �� �������
	bih.biCompression = BI_RGB; // ��� ������
	bih.biHeight = Height;
	bih.biWidth = Width;
	bih.biPlanes = 1; // ������ ���� 1
					  // � ��������� ���� �������� 0
	hFile = CreateFile(fname, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
	if (hFile == INVALID_HANDLE_VALUE)
		return;

	// ������� ���������
	WriteFile(hFile, &bfh, sizeof(bfh), &RW, NULL);
	WriteFile(hFile, &bih, sizeof(bih), &RW, NULL);

	// ������� �������
	WriteFile(hFile, Palette, 1024, &RW, NULL);
	for (i = 0; i < Height; i++)
	{
		for (j = 0; j < Width; j++)
		{
			WriteFile(hFile, &color, sizeof(color), &RW, NULL);
		}
		// ��������� �� �������
		WriteFile(hFile, Palette, Width % 4, &RW, NULL);
	}

	CloseHandle(hFile);
}

// �������� �������� � ������� bmp 8 ���
void CreateBmp8(char *fname, BYTE color)
{
	HANDLE hFile;
	DWORD RW;
	int i, j;

	// ������� ������ ���������
	BITMAPFILEHEADER bfh;
	BITMAPINFOHEADER bih;
	RGBQUAD Palette[256]; // �������

	// ����� � ��� ����� �������� �������� 35 x 50 ��������
	int Width = 35;
	int Height = 50;

	// �������� ��
	memset(&bfh, 0, sizeof(bfh));
	bfh.bfType = 0x4D42;							  // ���������, ��� ��� bmp 'BM'
	bfh.bfOffBits = sizeof(bfh) + sizeof(bih) + 1024; // ������� �������� 1Kb, �� �� ��� ����������� �� �����
	bfh.bfSize = bfh.bfOffBits +
				 sizeof(color) * Width * Height +
				 Height * ((3 * Width) % 4); // ��������� ������ ��������� �����

	memset(&bih, 0, sizeof(bih));
	bih.biSize = sizeof(bih);	// ��� ��������
	bih.biBitCount = 8;			// 16 ��� �� �������
	bih.biCompression = BI_RGB; // ��� ������
	bih.biHeight = Height;
	bih.biWidth = Width;
	bih.biPlanes = 1; // ������ ���� 1
					  // � ��������� ���� �������� 0
	hFile = CreateFile(fname, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
	if (hFile == INVALID_HANDLE_VALUE)
		return;

	// ������� ���������
	WriteFile(hFile, &bfh, sizeof(bfh), &RW, NULL);
	WriteFile(hFile, &bih, sizeof(bih), &RW, NULL);

	// �������� � ������� �������
	memset(&Palette[0], 0, sizeof(RGBQUAD));
	for (i = 1; i < 256; i++)
	{
		Palette[i].rgbBlue = Palette[i - 1].rgbBlue + 20;
		Palette[i].rgbGreen = Palette[i - 1].rgbGreen + 30;
		Palette[i].rgbRed = Palette[i - 1].rgbRed + 10;
	}
	WriteFile(hFile, Palette, 256 * sizeof(RGBQUAD), &RW, NULL);
	for (i = 0; i < Height; i++)
	{
		for (j = 0; j < Width; j++)
		{
			WriteFile(hFile, &color, sizeof(color), &RW, NULL);
		}
		// ��������� �� �������
		WriteFile(hFile, Palette, (3 * Width) % 4, &RW, NULL);
	}

	CloseHandle(hFile);
}

BOOL Convert256To24(char *fin, char *fout)
{
	BITMAPFILEHEADER bfh;
	BITMAPINFOHEADER bih;
	int Width, Height;
	RGBQUAD Palette[256];
	BYTE *inBuf;
	RGBTRIPLE *outBuf;
	HANDLE hIn, hOut;
	DWORD RW;
	DWORD OffBits;
	int i, j;

	hIn = CreateFile(fin, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
	if (hIn == INVALID_HANDLE_VALUE)
		return FALSE;

	hOut = CreateFile(fout, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
	if (hOut == INVALID_HANDLE_VALUE)
	{
		CloseHandle(hIn);
		return FALSE;
	}

	// ������� ������
	ReadFile(hIn, &bfh, sizeof(bfh), &RW, NULL);
	ReadFile(hIn, &bih, sizeof(bih), &RW, NULL);
	ReadFile(hIn, Palette, 256 * sizeof(RGBQUAD), &RW, NULL);

	// ��������� ��������� �� ������ ������
	SetFilePointer(hIn, bfh.bfOffBits, NULL, FILE_BEGIN);

	Width = bih.biWidth;
	Height = bih.biHeight;
	OffBits = bfh.bfOffBits;

	// ������� ������
	inBuf = new BYTE[Width];
	outBuf = new RGBTRIPLE[Width];

	// �������� ���������
	bfh.bfOffBits = sizeof(bfh) + sizeof(bih); // �� ����� ������ �������
	bih.biBitCount = 24;
	bfh.bfSize = bfh.bfOffBits + 4 * Width * Height + Height * (Width % 4); // ������ �����
	// � ��������� �� ��������

	// ������� ���������
	WriteFile(hOut, &bfh, sizeof(bfh), &RW, NULL);
	WriteFile(hOut, &bih, sizeof(bih), &RW, NULL);

	// ������ ���������������
	for (i = 0; i < Height; i++)
	{
		ReadFile(hIn, inBuf, Width, &RW, NULL);
		for (j = 0; j < Width; j++)
		{
			outBuf[j].rgbtRed = Palette[inBuf[j]].rgbRed;
			outBuf[j].rgbtGreen = Palette[inBuf[j]].rgbGreen;
			outBuf[j].rgbtBlue = Palette[inBuf[j]].rgbBlue;
		}
		WriteFile(hOut, outBuf, sizeof(RGBTRIPLE) * Width, &RW, NULL);

		// ����� ��� ������������
		WriteFile(hOut, Palette, Width % 4, &RW, NULL);
		SetFilePointer(hIn, (3 * Width) % 4, NULL, FILE_CURRENT);
	}

	delete inBuf;
	delete outBuf;
	CloseHandle(hIn);
	CloseHandle(hOut);

	return TRUE;
}