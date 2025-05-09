"use client";

import React, { useRef } from 'react';

interface FileInputProps {
    onFileSelect: (file: File) => void;
    file: File | null;
}

const FileInput: React.FC<FileInputProps> = ({ onFileSelect, file }) => {
    // const [dragging, setDragging] = useState(false);
    const inputFile = useRef<HTMLInputElement>(null);

    const handleDragEnter = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        // setDragging(true);
    };

    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        // setDragging(false);
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        // setDragging(false);

        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            onFileSelect(e.dataTransfer.files[0]);
            e.dataTransfer.clearData();
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            onFileSelect(e.target.files[0]);
        }
    };

    function fileSizeToText(size: number) {
        if (size < 1024) return size + ' bytes';
        const i = Math.floor(Math.log(size) / Math.log(1024));
        return (size / Math.pow(1024, i)).toFixed(2) + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i];
    }

    return (
        <div
            onClick={() => {
                if (inputFile.current) inputFile.current.click()
            }} 
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            className="w-full min-h-20 border border-gray-400 hover:bg-slate-100 border-dashed rounded-lg p-4 flex flex-col items-center justify-center transition-colors gap-3"
        >
            <input
                ref={inputFile}
                type="file"
                onChange={handleFileChange}
                style={{ display: 'none' }}
                id="fileInput"
            />
            {
                (!file) ? (
                    <span className="text-gray-700 text-sm">Click here to upload the file or drop your file here</span>
                ) : (
                    <div className="w-full flex gap-3 items-center">
                        <div className="relative w-10">
                            <p className="text-3xl">📝</p>
                        </div>    
                        <div className="grow flex flex-col gap-1">
                            <span className="text-gray-700 text-sm">{file.name}</span>
                            <span className="text-gray-700 text-sm">Size: {fileSizeToText(file.size)}</span>
                        </div>
                    </div>
                    
                )
            }
            
        </div>
    );
};

export default FileInput;