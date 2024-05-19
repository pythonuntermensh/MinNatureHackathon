"use client";

import ClassifiedFiles from "@/components/classified-files";
import PhotoUpload from "@/components/photo-upload";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export default function Page() {
  const [isChoosingFiles, setIsChoosingFiles] = useState(true);
  const [classifiedFiles, setClassifiedFiles] = useState<{
    [key: string]: string;
  }>({});
  const [isFilesClassifying, setIsFilesClassifying] = useState(false);

  return (
    <div className="flex justify-center items-center overflow-y-auto h-full p-2">
      <div className="p-4 rounded-lg bg-zinc-100 min-w-[100%] md:min-w-[50%] shadow-lg">
        <div className="w-fit mb-2">
          <Link href={"/"} className="w-fit">
            <ArrowLeft className="w-8 h-8 rounded-full hover:bg-zinc-300 transition" />
          </Link>
        </div>
        {isChoosingFiles ? (
          <>
            <p className="text-sm font-semibold text-zinc-700 w-[80%]">
              Выберите фото, которые необходимо классифицировать.
            </p>
            <PhotoUpload />
          </>
        ) : (
          <ClassifiedFiles />
        )}
      </div>
    </div>
  );
}
