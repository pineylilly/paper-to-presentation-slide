"use client";

import FileInput from "./components/Form/FileInput";
import { useEffect, useState } from "react";
import { getMarkdown, getSlide, inferencePaper } from "./utils/action";
import { InferenceResponseWithDate } from "./utils/type";

export default function Home() {
  const [inputFile, setInputFile] = useState<File | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  const [currentInference, setCurrentInference] = useState<InferenceResponseWithDate | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [markdown, setMarkdown] = useState<string | null>(null);
  const [slide, setSlide] = useState<File | null>(null);

  const [inferenceData, setInferenceData] = useState<InferenceResponseWithDate[]>([]);

  async function checkAndSetFile(file: File) {
    console.log(file)
    if (file.type !== "application/pdf") {
        alert("Only PDF files are allowed");
        return
    }
    setInputFile(file);
  }

  async function inference() {
    if (!inputFile) {
      alert("Please upload a file first");
      return;
    }
    setIsRunning(true);
    try {
      const data: InferenceResponseWithDate = {...await inferencePaper(inputFile), created_at: new Date().toISOString()};
      console.log(data);
      setCurrentInference(data);
      // Add to local storage
      const existingData = localStorage.getItem("inferenceData");
      const newData = existingData ? [data, ...JSON.parse(existingData)] : [data];
      localStorage.setItem("inferenceData", JSON.stringify(newData));
      setInferenceData(newData);

    } catch (error) {
      console.error("Error during inference:", error);
      alert(error)
    } finally {
      setIsRunning(false);
    }
  }

  async function getInferenceData() {
    if (!currentInference) return;

    setIsLoading(true);
    try {
      const markdown = await getMarkdown(currentInference.id);
      setMarkdown(markdown);
      const slide = await getSlide(currentInference.id);
      setSlide(slide);
    } catch (error) {
      console.error("Error fetching inference data:", error);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    const existingData = localStorage.getItem("inferenceData");
    if (existingData) {
      setInferenceData(JSON.parse(existingData));
    }
  }, [])

  useEffect(() => {
    if (currentInference) getInferenceData();
  }, [currentInference]);

  return (
    <div className="w-full min-h-screen bg-[#f9f9f9] flex flex-col items-center gap-10 px-16 py-10">
      <h1 className="text-3xl text-center font-bold">Academic Papers To Presentation Slides Generator</h1>
      <div className="w-full md:w-4/5 grid grid-cols-1 md:grid-cols-2 gap-4">
        
        {
          (currentInference && !isLoading) && (
            <div className="w-full col-span-2 h-fit flex flex-col items-center gap-4 border border-gray-300 rounded-xl p-4 bg-[#f9f9f9]">
              <h3 className="font-bold">Result</h3>
              <p className="w-full text-left">Markdown</p>
              <textarea
                className="w-full h-60 border border-gray-300 rounded-xl p-2 bg-white whitespace-pre-line"
                value={markdown || ""}
                readOnly
              />
              <p className="w-full text-left">Slide</p>
              <div className="h-[30rem] aspect-video border border-gray-300 rounded-xl p-2 bg-white flex items-center justify-center">
                {
                  (slide) ?
                  <iframe src={URL.createObjectURL(slide)} className="w-full h-full" /> :
                  <p>No slide available</p>
                }
              </div>
            </div>
          )
        }

        <div className="w-full flex flex-col items-center gap-4 border border-gray-300 rounded-xl p-4 bg-[#f9f9f9]">
          <h3 className="font-bold">
            Upload your academic paper in PDF format
          </h3>
          <FileInput onFileSelect={(file) => checkAndSetFile(file)} file={inputFile} />
          {
            (!inputFile) &&
            <button
            className="bg-slate-400 text-white px-3 py-2 rounded-lg transition-colors text-sm"
            >
              Generate Slides
            </button>
          }
          {
            (inputFile && !isRunning) &&
            <button
            className="bg-indigo-600 text-white px-3 py-2 rounded-lg hover:bg-indigo-700 transition-colors text-sm"
            onClick={() => {
              if(inputFile) inference();
            }}
            disabled={!inputFile}
            >
              Generate Slides
            </button>
          }
          {
            (isRunning) &&
            <button
            className="bg-slate-400 text-white px-3 py-2 rounded-lg transition-colors text-sm"
            >
              Generating Slides
            </button>
          }
          
        </div>
        <div className="w-full h-fit flex flex-col items-center gap-4 border border-gray-300 rounded-xl p-4 bg-[#f9f9f9]">
          <h3 className="font-bold">
            History
          </h3>
          {
            inferenceData.length > 0 ?
            <div className="w-full flex flex-col gap-2">
              {
                inferenceData.map((data, index) => (
                  <div 
                    key={index} 
                    className="w-full flex flex-col gap-2 border border-gray-300 rounded-xl p-4 bg-[#f9f9f9] hover:bg-slate-100"
                    onClick={() => setCurrentInference(data)}
                  >
                    <p className="">{data.filename}</p>
                    <p className="text-sm text-gray-500">{new Date(data.created_at).toLocaleString()}</p>
                  </div>
                ))
              }
            </div>
            :
            <p>No history available</p>
          }
        </div>
      </div>
    </div>
  );
}
