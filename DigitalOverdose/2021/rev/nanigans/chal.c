#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <Python.h>
#include <stdbool.h>

EFI_STATUS efi_main (EFI_HANDLE ImageHandle, EFI_SYSTEM_TABLE *SystemTable) {
    InitializeLib(ImageHandle, SystemTable);
    Print(L"String blah blah blah \n\r");

    EFI_FILE* Kernel = LoadFile(NULL, L"kernel.elf", ImageHandle, SystemTable);
    if (Kernel == NULL){
        Print(L"Could not load kernel \n\r");
    }
    else{
        Print(L"Kernel Loaded Successfully \n\r");
    }

    Elf64_Ehdr header;
    {
        UINTN FileInfoSize;
        EFI_FILE_INFO* FileInfo;
        Kernel->GetInfo(Kernel, &gEfiFileInfoGuid, &FileInfoSize, NULL);
        SystemTable->BootServices->AllocatePool(EfiLoaderData, FileInfoSize, (void**)&FileInfo);
        Kernel->GetInfo(Kernel, &gEfiFileInfoGuid, &FileInfoSize, (void**)&FileInfo);

        UINTN size = sizeof(header);
        Kernel->Read(Kernel, &size, &header);
    }

    if (
        memcmp(&header.e_ident[EI_MAG0], ELFMAG, SELFMAG) != 0 ||
        header.e_ident[EI_CLASS] != ELFCLASS64 ||
        header.e_ident[EI_DATA] != ELFDATA2LSB ||
        header.e_type != ET_EXEC ||
        header.e_machine != EM_X86_64 ||
        header.e_version != EV_CURRENT
    )
    {
        Print(L"kernel format is bad\r\n");
    }
    else
    {
        Print(L"kernel header successfully verified\r\n");
    }

    Elf64_Phdr* phdrs;
    {
        Kernel->SetPosition(Kernel, header.e_phoff);
        UINTN size = header.e_phnum * header.e_phentsize;
        SystemTable->BootServices->AllocatePool(EfiLoaderData, size, (void**)&phdrs);
        Kernel->Read(Kernel, &size, phdrs);
    }

    for (
        Elf64_Phdr* phdr = phdrs;
        (char*)phdr < (char*)phdrs + header.e_phnum * header.e_phentsize;
        phdr = (Elf64_Phdr*)((char*)phdr + header.e_phentsize)
    )
    {
        switch (phdr->p_type){
            case PT_LOAD:
            {
                int pages = (phdr->p_memsz + 0x1000 - 1) / 0x1000;
                Elf64_Addr segment = phdr->p_paddr;
                SystemTable->BootServices->AllocatePages(AllocateAddress, EfiLoaderData, pages, &segment);

                Kernel->SetPosition(Kernel, phdr->p_offset);
                UINTN size = phdr->p_filesz;
                Kernel->Read(Kernel, &size, (void*)segment);
                break;
            }
        }
    }

    Print(L"Kernel Loaded\n\r");
    

    PSF1_FONT* newFont = LoadPSF1Font(NULL, L"zap-light16.psf", ImageHandle, SystemTable);
    if (newFont == NULL){
        Print(L"Font is not valid or is not found\n\r");
    }
    else
    {
        Print(L"Font found. char size = %d\n\r", newFont->psf1_Header->charsize);
    }
    

    Framebuffer* newBuffer = InitializeGOP();

    Print(L"Base: 0x%x\n\rSize: 0x%x\n\rWidth: %d\n\rHeight: %d\n\rPixelsPerScanline: %d\n\r", 
    newBuffer->BaseAddress, 
    newBuffer->BufferSize, 
    newBuffer->Width, 
    newBuffer->Height, 
    newBuffer->PixelsPerScanLine);

    EFI_MEMORY_DESCRIPTOR* Map = NULL;
    UINTN MapSize, MapKey;
    UINTN DescriptorSize;
    UINT32 DescriptorVersion;
    {
        
        SystemTable->BootServices->GetMemoryMap(&MapSize, Map, &MapKey, &DescriptorSize, &DescriptorVersion);
        SystemTable->BootServices->AllocatePool(EfiLoaderData, MapSize, (void**)&Map);
        SystemTable->BootServices->GetMemoryMap(&MapSize, Map, &MapKey, &DescriptorSize, &DescriptorVersion);

    }

    EFI_CONFIGURATION_TABLE* configTable = SystemTable->ConfigurationTable;
    void* rsdp = NULL; 
    EFI_GUID Acpi2TableGuid = ACPI_20_TABLE_GUID;

    for (UINTN index = 0; index < SystemTable->NumberOfTableEntries; index++){
        if (CompareGuid(&configTable[index].VendorGuid, &Acpi2TableGuid)){
            if (strcmp((CHAR8*)"RSD PTR ", (CHAR8*)configTable->VendorTable, 8)){
                rsdp = (void*)configTable->VendorTable;
                //break;
            }
        }
        configTable++;
    }

    void (*KernelStart)(BootInfo*) = ((__attribute__((sysv_abi)) void (*)(BootInfo*) ) header.e_entry);

    BootInfo bootInfo;
    bootInfo.framebuffer = newBuffer;
    bootInfo.psf1_Font = newFont;
    bootInfo.mMap = Map;
    bootInfo.mMapSize = MapSize;
    bootInfo.mMapDescSize = DescriptorSize;
    bootInfo.rsdp = rsdp;

    SystemTable->BootServices->ExitBootServices(ImageHandle, MapKey);

    KernelStart(&bootInfo);

    return EFI_SUCCESS; // Exit the UEFI application
}

char* aa;

typedef struct {char* pTr; size_t lEn;} snafu;

struct snafu {
    unsigned cNt
    char* pTr
    size_t len
} A;

int memcmp(const void* aptr, const void* bptr, size_t n){
    const unsigned char* a = aptr, *b = bptr;
    for (size_t i = 0; i < n; i++){
        if (a[i] < b[i]) return -1;
        else if (a[i] > b[i]) return 1;
    }
    return 0;
}

void aaa(int* n){aa = (char) 0[*n];} 

#define p1 0xfacce
#define fastcopy(x,y,z) /*x,y,z*/

#define fg 0xf1a

int main(void) {
    #ifndef ur_mom
        printf("Try looking in the source code instead of compiling\n");
    #endif
}

#include <efi.h>
#include <efilib.h>
#include <elf.h>

typedef unsigned long long size_t;

typedef struct {
    void* BaseAddress;
    size_t BufferSize;
    unsigned int Width;
    unsigned int Height;
    unsigned int PixelsPerScanLine;
} Framebuffer;

#define PSF1_MAGIC0 0x36
#define PSF1_MAGIC1 0x04

typedef struct {
    unsigned char magic[2];
    unsigned char mode;
    unsigned char charsize;
} PSF1_HEADER;

typedef struct {
    PSF1_HEADER* psf1_Header;
    void* glyphBuffer;
} PSF1_FONT;

#define fp1 0x444f7b

Framebuffer framebuffer;
Framebuffer* InitializeGOP(){
    EFI_GUID gopGuid = EFI_GRAPHICS_OUTPUT_PROTOCOL_GUID;
    EFI_GRAPHICS_OUTPUT_PROTOCOL* gop;
    EFI_STATUS status;

    status = uefi_call_wrapper(BS->LocateProtocol, 3, &gopGuid, NULL, (void**)&gop);
    if(EFI_ERROR(status)){
        Print(L"Unable to locate GOP\n\r");
        return NULL;
    }
    else
    {
        Print(L"GOP located\n\r");
    }

    framebuffer.BaseAddress = (void*)gop->Mode->FrameBufferBase;
    framebuffer.BufferSize = gop->Mode->FrameBufferSize;
    framebuffer.Width = gop->Mode->Info->HorizontalResolution;
    framebuffer.Height = gop->Mode->Info->VerticalResolution;
    framebuffer.PixelsPerScanLine = gop->Mode->Info->PixelsPerScanLine;

    return &framebuffer;
    
}

EFI_FILE* LoadFile(EFI_FILE* Directory, CHAR16* Path, EFI_HANDLE ImageHandle, EFI_SYSTEM_TABLE* SystemTable){
    EFI_FILE* LoadedFile;

    EFI_LOADED_IMAGE_PROTOCOL* LoadedImage;
    SystemTable->BootServices->HandleProtocol(ImageHandle, &gEfiLoadedImageProtocolGuid, (void**)&LoadedImage);

    EFI_SIMPLE_FILE_SYSTEM_PROTOCOL* FileSystem;
    SystemTable->BootServices->HandleProtocol(LoadedImage->DeviceHandle, &gEfiSimpleFileSystemProtocolGuid, (void**)&FileSystem);

    if (Directory == NULL){
        FileSystem->OpenVolume(FileSystem, &Directory);
    }

    EFI_STATUS s = Directory->Open(Directory, &LoadedFile, Path, EFI_FILE_MODE_READ, EFI_FILE_READ_ONLY);
    if (s != EFI_SUCCESS){
        return NULL;
    }
    return LoadedFile;

}

#define fp2 0x733075526333

PSF1_FONT* LoadPSF1Font(EFI_FILE* Directory, CHAR16* Path, EFI_HANDLE ImageHandle, EFI_SYSTEM_TABLE* SystemTable)
{
    EFI_FILE* font = LoadFile(Directory, Path, ImageHandle, SystemTable);
    if (font == NULL) return NULL;

    PSF1_HEADER* fontHeader;
    SystemTable->BootServices->AllocatePool(EfiLoaderData, sizeof(PSF1_HEADER), (void**)&fontHeader);
    UINTN size = sizeof(PSF1_HEADER);
    font->Read(font, &size, fontHeader);

    if (fontHeader->magic[0] != PSF1_MAGIC0 || fontHeader->magic[1] != PSF1_MAGIC1){
        #define fp4 0x7d
        return NULL;
    }

    UINTN glyphBufferSize = fontHeader->charsize * 256;
    if (fontHeader->mode == 1) { //512 glyph mode
        glyphBufferSize = fontHeader->charsize * 512;
    }

    void* glyphBuffer;
    {
        font->SetPosition(font, sizeof(PSF1_HEADER));
        SystemTable->BootServices->AllocatePool(EfiLoaderData, glyphBufferSize, (void**)&glyphBuffer);
        font->Read(font, &glyphBufferSize, glyphBuffer);
    }

    PSF1_FONT* finishedFont;
    SystemTable->BootServices->AllocatePool(EfiLoaderData, sizeof(PSF1_FONT), (void**)&finishedFont);
    finishedFont->psf1_Header = fontHeader;
    finishedFont->glyphBuffer = glyphBuffer;
    return finishedFont;

}

typedef struct {
    Framebuffer* framebuffer;
    PSF1_FONT* psf1_Font;
    EFI_MEMORY_DESCRIPTOR* mMap;
    UINTN mMapSize;
    UINTN mMapDescSize;
    void* rsdp;
} BootInfo;

UINTN strcmp(CHAR8* a, CHAR8* b, UINTN length){
    for (UINTN i = 0; i < length; i++){
        if (*a != *b) return 0;
    }
    #define fp3 0x5f406e616c79333173

    return 1;
}

