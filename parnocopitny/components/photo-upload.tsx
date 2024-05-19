"use client";

import { ChevronRight, Trash, Upload } from "lucide-react";
import { Dispatch, SetStateAction, useState } from "react";
import { cn } from "@/lib/utils";
import { v4 as uuidv4 } from 'uuid';
import { Button } from "./ui/button";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"

const FileUpload = () => {
  const [files, setFiles] = useState<{ id: string; file: File }[]>([]);
  const [isFilesClassifying, setIsFilesClassifying] = useState(false);

  const handleFileChange = (e: any) => {
    const newFiles = Array.from(e.target.files as File[]).map((file: File) => ({
      id: uuidv4(),
      file: file,
    }));
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleFileDelete = (idToDelete: string) => {
    setFiles((prevFiles) => prevFiles.filter((file) => file.id !== idToDelete));
  };

  const handleSubmit = () => {
    setIsFilesClassifying(true);
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file.file);
    });
    //TODO create backend call in http folder
    // classifyFiles(formData).then((res) => {
    //   setClassifiedFiles(res.data.message);
    // }).finally(() => setIsFilesClassifying(false));
    // setIsChoosingFiles((prevState) => !prevState);
  };

  return (
    <div>
      <div className={cn("flex items-center justify-center mb-2", files.length === 0 && "h-full")}>
        <label
          className={cn(
            files.length > 0
              ? "flex items-center justify-center gap-x-3 text-white my-3 button w-48 h-16 bg-blue-500 rounded-lg cursor-pointer select-none active:translate-y-2  active:[box-shadow:0_0px_0_0_#1b6ff8,0_0px_0_0_#1b70f841] active:border-b-[0px] transition-all duration-150 [box-shadow:0_10px_0_0_#1b6ff8,0_15px_0_0_#1b70f841] border-b-[1px] border-blue-400"
              : "flex flex-col items-center jusitfy-center border-2 border-dashed p-14 shadow-lg md:hover:scale-[1.05] transition m-5 text-zinc-500 rounded-md hover:cursor-pointer "
          )}
          htmlFor="document-file"
        >
          <p className="text-center">
            {files.length > 0 ? "Добавить файлы..." : "Выбрать файлы..."}
          </p>
          <Upload className={cn(files.length === 0 && "text-zinc-400 w-10 h-10")} />
        </label>
        <input
          key={files.length}
          type="file"
          accept="image/*"
          id="document-file"
          multiple
          onChange={handleFileChange}
          hidden
        />
      </div>

      <ScrollArea className={cn("h-60 md:h-72 pr-2", files.length === 0 && "hidden")}>
        {files.map((file, index) => (
          <div
            key={index}
            className="flex items-center justify-between py-3 my-1 border-y-2 border-dashed border-zinc-400"
          >
            <p className="max-w-[80%] line-clamp-2">{file.file.name}</p>
            <Trash
              onClick={() => handleFileDelete(file.id)}
              className="text-rose-500 w-7 h-7 cursor-pointer"
            />
          </div>
        ))}
        <ScrollBar orientation="horizontal" />
        <ScrollBar orientation="vertical" />
      </ScrollArea>

      {files.length > 0 && (
        <div className="mt-5 flex justify-end">
          <Button
            className="flex items-center group bg-zinc-300 ml-auto text-black hover:bg-zinc-400"
            onClick={handleSubmit}
          >
            <p>Подтвердить</p>
            <ChevronRight className="text-zinc-500 group-hover:translate-x-1 transition" />
          </Button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
