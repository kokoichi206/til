<?php

namespace App\Http\Requests\Type;

use App\Http\Requests\RegisterRepositoryRequest;

class RegisterRepositoryRequestType
{
    public string $name;
    public int $page;

    public function __construct(RegisterRepositoryRequest $request)
    {
        $this->name = $request->input('name');
        $this->page = $request->input('page') ?? 1;
    }
}
