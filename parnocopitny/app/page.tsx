"use client";

import { DeerModelViewer, TableModelViewer } from "@/components/model-viewer";
import { Button } from "@/components/ui/button";
import { Carrot, FolderArchive, Image, MoveUp } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export default function Home() {
  const [sizes, setSizes] = useState<number[]>([0.25, 0.25, 0.25])
  return (
    <div className="flex flex-col h-full items-center justify-center text-white p-2">
      <div className="flex flex-col gap-y-2 items-center">
        <p className="text-3xl md:text-6xl font-bold bg-gradient-to-r from-green-600 via-green-700 to-emerald-600 text-transparent bg-clip-text bg-300% animate-gradient">
          SHA-256
        </p>
        <p className="text-lg md:text-xl text-center">Кейс «Классификация парнокопытных»</p>
        <div className="flex items-center justify-center flex-col gap-y-2 md:flex-row md:gap-x-2 p-2">
          <Link href={"/upload-photos"}>
            <Button className="flex items-center gap-x-2 bg-white text-emerald-500 hover:bg-neutral-100">
              <p>Загрузить фото</p>
              <Image />
            </Button>
          </Link>
          <Link href={"/upload-archives"}>
            <Button className="flex items-center gap-x-2 bg-emerald-500 text-white hover:bg-emerald-600">
              <p>Загрузить архив с фото</p>
              <FolderArchive />
            </Button>
          </Link>
        </div>
      </div>

      <div className="flex flex-col items-center justify-center w-full">
        <div className="flex flex-col md:flex-row gap-x-1 items-center">
          <DeerModelViewer fileName={"/3.glb"} sizes={sizes} />
          <TableModelViewer fileName={"/7.glb"} />
        </div>
        
        <Button className="flex items-center gap-x-2 bg-yellow-400 hover:bg-yellow-300 text-neutral-800" onClick={() => setSizes([Math.random(), Math.random(), Math.random()])}>
          <p>Покормить Леонида</p>
          <Carrot />
        </Button>
      </div>
    </div>
  );
}
