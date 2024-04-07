<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('gh_name')->unique('unique_gh_name')->nullable();
        });

        Schema::create('repositories', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->string('name');
            $table->string('description')->nullable();
            $table->string('license')->nullable();
            $table->integer('open_issues');
            $table->string('gh_user_name');
            $table->boolean('fork');
            $table->timestamps();

            // users を使い外部キー制約としたい場合。
            // $table->foreign('gh_user_name')->references('gh_name')->on('users');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('repositories');

        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('gh_name');
        });
    }
};
