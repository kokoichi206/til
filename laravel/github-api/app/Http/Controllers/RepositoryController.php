<?php

namespace App\Http\Controllers;

use App\Http\Resources\RepositoriesResource;
use App\Models\Repository;

class RepositoryController extends Controller
{
    public function getRepositories()
    {
        $repositories = Repository::all();
        $total = Repository::count();

        $res['repositories'] = $repositories;
        $res['total'] = $total;

        // dd($res);
        return RepositoriesResource::make($res);
    }
}
