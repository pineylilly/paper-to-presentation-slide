"use server";

import { InferenceResponse } from "./type";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const inferencePaper = async (file: File): Promise<InferenceResponse> => {
    console.log(file)
    
    // Create a FormData object to send the file
    const formData = new FormData();
    formData.append("file", file);

    // Send the file to the server using fetch
    const response = await fetch(`${API_URL}/process`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error(await response.text());
    }

    const data = await response.json();
    console.log(data)
    return data;
}


export const getMarkdown = async (id: string): Promise<string> => {
    const response = await fetch(`${API_URL}/process/${id}/markdown`, {
        method: "GET",
    });

    if (!response.ok) {
        throw new Error(await response.text());
    }

    const data = await response.json();
    return data.data as string;
}

export const getSlide = async (id: string): Promise<File> => {
    const response = await fetch(`${API_URL}/process/${id}/slide`, {
        method: "GET",
    });

    if (!response.ok) {
        throw new Error(await response.text());
    }

    const data = await response.blob();
    return new File([data], `${id}.pdf`, { type: "application/pdf" });
}