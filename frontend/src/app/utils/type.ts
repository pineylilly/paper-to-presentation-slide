export interface InferenceResponse {
    filename: string;
    is_compile_success: boolean;
    id: string;
}

export interface InferenceResponseWithDate extends InferenceResponse {
    created_at: string;
}