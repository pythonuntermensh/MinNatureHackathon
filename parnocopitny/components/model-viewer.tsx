"use client";

import { Canvas, useLoader, useFrame } from "@react-three/fiber";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { OrbitControls, Center } from "@react-three/drei";
import { useRef } from "react";

const DeerModel = ({ fileName, sizes }: { fileName: string, sizes: number[] }) => {
  const myModel = useLoader(GLTFLoader, fileName);
  const modelRef = useRef();

  useFrame(() => {
    if (modelRef.current) {
      //@ts-ignore
      modelRef.current.rotation.y += 0.01; // Вращение модели вокруг её центра
    }
  });

  return (
    <primitive
      ref={modelRef}
      object={myModel.scene}
      scale={sizes} // Измените масштаб по необходимости
    />
  );
};

const TableModel = ({ fileName }: { fileName: string }) => {
  const myModel = useLoader(GLTFLoader, fileName);
  const modelRef = useRef();

  return (
    <primitive
      ref={modelRef}
      object={myModel.scene}
      scale={[0.8, 0.8, 0.8]} // Измените масштаб по необходимости
    />
  );
};

export const DeerModelViewer = ({ fileName, sizes }: { fileName: string, sizes: number[] }) => {
  return (
    <Canvas
      style={{ width: "100%", height: "250px" }}
      camera={{ position: [0, 0, 10], fov: 70 }} // Настройка камеры
    >
      <pointLight position={[10, -10, -10]} color="#48cc90" intensity={2000} />
      <pointLight position={[10, 10, 10]} color="#36e2e2" intensity={2000} />
      <pointLight position={[10, -10, 10]} color="#36e2e2" intensity={2000} />
      <pointLight position={[-10, 10, 10]} color="#36e2e2" intensity={2000} />
      <pointLight position={[-10, 10, -10]} color="#36e2e2" intensity={2000} />
      <Center>
        {" "}
        {/* Центрируем модель */}
        <DeerModel fileName={fileName} sizes={sizes} />
      </Center>
      <OrbitControls
        enableDamping={false}
        target={[0, 0, 0]} // Центрируем камеру на модель
      />
    </Canvas>
  );
};

export const TableModelViewer = ({ fileName }: { fileName: string }) => {
  return (
    <Canvas
      style={{ height: "175px" }}
      camera={{ position: [0, 0, 10], fov: 50 }} // Настройка камеры
    >
      <pointLight position={[10, -10, -10]} color="#48cc90" intensity={2000} />
      <pointLight position={[10, 10, 10]} color="#36e2e2" intensity={2000} />
      <pointLight position={[10, -10, 10]} color="#36e2e2" intensity={2000} />
      <pointLight position={[-10, 10, 10]} color="#36e2e2" intensity={2000} />
      <pointLight position={[-10, 10, -10]} color="#36e2e2" intensity={2000} />
      <Center>
        {" "}
        {/* Центрируем модель */}
        <TableModel fileName={fileName} />
      </Center>
      <OrbitControls
        enableDamping={false}
        autoRotate={false}
        
        target={[0, 0, 0]} // Центрируем камеру на модель
      />
    </Canvas>
  );
};
