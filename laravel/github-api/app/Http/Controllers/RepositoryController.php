<?php

namespace App\Http\Controllers;

use App\Http\Requests\RegisterRepositoryRequest;
use App\Http\Resources\RepositoriesResource;
use App\Models\Repository;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;

class RepositoryController extends Controller
{
    private $base = "https://api.github.com";

    public function getRepositories()
    {
        $repositories = Repository::all();
        $total = Repository::count();

        $res['repositories'] = $repositories;
        $res['total'] = $total;

        return RepositoriesResource::make($res);
    }

    public function registerRepositories(RegisterRepositoryRequest $request)
    {
        $page = $request->page ?? 1;
        $res = Http::get("{$this->base}/users/{$request->name}/repos?page={$page}");
        if ($res->status() !== 200) {
            Log::error("github api error", ["status" => $res->status(), "body" => $res->body()]);
            return response()->json(['message' => 'ERROR'], $res->status());
        }

        $bulk = [];
        $repos = $res->json();
        for ($i = 0; $i < count($repos); $i++) {
            $repository = $repos[$i];
            $bulk[] = [
                'id' => Str::uuid(),
                'name' => $repository['name'],
                'description' => $repository['description'] ?? null,
                'license' => $repository['license']['spdx_id'] ?? null,
                'open_issues' => $repository['open_issues'],
                'gh_user_name' => $request->name,
                'fork' => $repository['fork'],
                'created_at' => now(),
                'updated_at' => now(),
            ];
        }

        Repository::insert($bulk);

        return response()->noContent(204);
    }
}
