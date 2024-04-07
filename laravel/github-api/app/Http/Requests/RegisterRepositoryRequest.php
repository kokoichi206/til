<?php

namespace App\Http\Requests;

use App\Http\Requests\Type\RegisterRepositoryRequestType;
use Illuminate\Foundation\Http\FormRequest;

class RegisterRepositoryRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    public function getParams(): RegisterRepositoryRequestType
    {
        return new RegisterRepositoryRequestType($this);
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'name' => 'required|string',
            'page' => 'nullable|integer',
        ];
    }
}
