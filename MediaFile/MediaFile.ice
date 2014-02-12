module MediaFile {
    sequence<byte> ByteString;
    dictionary<string, string> FFMPEGParamsMap;

    interface FileTransfer {
        void send(string filename, int offset, ByteString bytes);
        void removeFile(string filename);
        bool isFileExists(string filename);
        string convertToMp4(string filename);
    };
};
