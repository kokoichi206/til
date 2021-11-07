# 「Could not resolve all files for configuration」junit が読み込めない

Android Studio において、「test は実行できるが androidTest の実行ができない」という症状に陥りました。

その解決方法についてメモしておこうと思います。

[目次]

[:contents]

## 環境
```
- compose_version = '1.0.1'
- targetSdk 31
- kotlinCompilerVersion '1.5.21'
```

今回は環境設定に関する記事なので、以下に gradle ファイルを書き出しておこうと思います。

### プロジェクトレベルの build.gradle
```gralde
// Top-level build file where you can add configuration options common to all sub-projects/modules.
buildscript {
    ext {
        compose_version = '1.0.1'
    }
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:7.0.2"
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:1.5.21"
        classpath "com.google.dagger:hilt-android-gradle-plugin:2.38.1"
        // NOTE: Do not place your application dependencies here; they belong
        // in the individual module build.gradle files
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
```

### アプリケーションレベルの build.gradle

```gradle
plugins {
    id 'com.android.application'
    id 'kotlin-android'
    id 'kotlin-kapt'
    id 'dagger.hilt.android.plugin'
}
android {
    compileSdk 31

    defaultConfig {
        applicationId "io.kokoichi.sample.sakamichiapp"
        minSdk 23
        targetSdk 31
        versionCode 1
        versionName "1.0"
        buildConfigField("String", "API_KEY", API_KEY)

        testInstrumentationRunner "io.kokoichi.sample.sakamichiapp.HiltTestRunner"
        vectorDrawables {
            useSupportLibrary true
        }
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
        useIR = true
    }
    buildFeatures {
        compose true
    }
    composeOptions {
        kotlinCompilerExtensionVersion compose_version
        kotlinCompilerVersion '1.5.21'
    }
    packagingOptions {
        resources {
            excludes += '/META-INF/{AL2.0,LGPL2.1}'
        }
    }
}

dependencies {

    implementation 'androidx.core:core-ktx:1.6.0'
    implementation 'androidx.appcompat:appcompat:1.3.1'
    implementation 'com.google.android.material:material:1.4.0'
    implementation "androidx.compose.ui:ui:$compose_version"
    implementation "androidx.compose.material:material:$compose_version"
    implementation "androidx.compose.ui:ui-tooling-preview:$compose_version"
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.3.1'
    implementation 'androidx.activity:activity-compose:1.3.1'
    implementation 'androidx.test:runner:1.4.0'
    testImplementation 'junit:junit:4.13.2'
    debugImplementation "androidx.compose.ui:ui-tooling:$compose_version"

    // Compose dependencies
    implementation "androidx.lifecycle:lifecycle-viewmodel-compose:1.0.0-alpha07"
    implementation "androidx.navigation:navigation-compose:2.4.0-alpha08"
    implementation "com.google.accompanist:accompanist-flowlayout:0.17.0"

    // Retrofit
    def retrofit_version = '2.9.0'
    implementation "com.squareup.retrofit2:retrofit:$retrofit_version"
    implementation "com.squareup.retrofit2:converter-gson:$retrofit_version"
    implementation 'com.squareup.retrofit2:adapter-rxjava2:2.4.0'
    implementation "com.squareup.okhttp3:okhttp:4.9.0"
    implementation "com.squareup.okhttp3:logging-interceptor:4.9.0"
    implementation "com.squareup.retrofit2:retrofit-mock:$retrofit_version"

    // Timber
    implementation 'com.jakewharton.timber:timber:4.7.1'

    // Coroutines
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.4.3'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.4.3'

    // Coroutine Lifecycle Scopes
    implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:2.3.1"
    implementation "androidx.lifecycle:lifecycle-runtime-ktx:2.4.0"

    // Coil
    implementation("io.coil-kt:coil-compose:1.4.0")

    //Dagger - Hilt
    implementation "com.google.dagger:hilt-android:2.38.1"
    kapt "com.google.dagger:hilt-android-compiler:2.37"
    implementation "androidx.hilt:hilt-lifecycle-viewmodel:1.0.0-alpha03"
    kapt "androidx.hilt:hilt-compiler:1.0.0"
    implementation 'androidx.hilt:hilt-navigation-compose:1.0.0-alpha03'

    androidTestImplementation 'com.google.dagger:hilt-android-testing:2.37'
    kaptAndroidTest 'com.google.dagger:hilt-android-compiler:2.37'

    // Local Unit Tests
    implementation "androidx.test:core:1.4.0"
    testImplementation "junit:junit:4.13.2"
    testImplementation "org.hamcrest:hamcrest-all:1.3"
    testImplementation "androidx.arch.core:core-testing:2.1.0"
    testImplementation "org.robolectric:robolectric:4.5.1"
    testImplementation "org.jetbrains.kotlinx:kotlinx-coroutines-test:1.5.0"
    testImplementation "com.google.truth:truth:1.1.3"
    testImplementation "com.squareup.okhttp3:mockwebserver:4.9.1"
    testImplementation "io.mockk:mockk:1.12.0"
    testImplementation "org.robolectric:robolectric:4.5.1"
    testImplementation("org.assertj:assertj-core:3.21.0")

    // Instrumented Unit Tests
    androidTestImplementation "junit:junit:4.13.2"
    androidTestImplementation "org.jetbrains.kotlinx:kotlinx-coroutines-test:1.5.0"
    androidTestImplementation "androidx.arch.core:core-testing:2.1.0"
    androidTestImplementation "com.google.truth:truth:1.1.3"
    androidTestImplementation 'androidx.test.ext:junit:1.1.3'
    androidTestImplementation 'androidx.test:core-ktx:1.4.0'
    androidTestImplementation "com.squareup.okhttp3:mockwebserver:4.9.1"
    androidTestImplementation "io.mockk:mockk-android:1.12.0"
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.4.0'
    androidTestImplementation "androidx.compose.ui:ui-test-junit4:$compose_version"

    // Action bar helper
    implementation "com.google.accompanist:accompanist-systemuicontroller:0.17.0"
}
```

## 症状
- test は実行できる
- androidTest の実行ができない
  - 最初から用意されてるテストすら実行できない

### エラーメッセージ
androidTest 実行時のエラーメッセージを抜粋して記述します。

`junit:junit:4.13.` と `junit:junit:4.12.` に依存するパッケージがあり、その読み込みの衝突が起こった結果、どちらも読み込めてないのかな、と思いました。

```
4: Task failed with an exception.
-----------
* What went wrong:
Execution failed for task ':app:mergeDebugAndroidTestNativeLibs'.
> Could not resolve all files for configuration ':app:debugAndroidTestRuntimeClasspath'.
   > Could not resolve junit:junit:4.13.2.
     Required by:
         project :app
         project :app > com.google.truth:truth:1.1.3
      > Cannot find a version of 'junit:junit' that satisfies the version constraints:
           Dependency path 'Sakamichi app:app:unspecified' --> 'junit:junit:4.13.2'

...
 > Could not resolve junit:junit:{strictly 4.12}.
     Required by:
         project :app
      > Cannot find a version of 'junit:junit' that satisfies the version constraints:
           Dependency path 'Sakamichi app:app:unspecified' --> 'junit:junit:4.13.2'
           Constraint path 'Sakamichi app:app:unspecified' --> 'junit:junit:{strictly 4.12}' because of the following reason: debugRuntimeClasspath uses version 4.12
           Dependency path 'Sakamichi app:app:unspecified' --> 'com.google.dagger:hilt-android-testing:2.37' (runtime) --> 'junit:junit:4.13'
           Dependency path 'Sakamichi app:app:unspecified' --> 'androidx.arch.core:core-testing:2.1.0' (runtime) --> 'junit:junit:4.12'
           Dependency path 'Sakamichi app:app:unspecified' --> 'com.google.truth:truth:1.1.3' (runtime) --> 'junit:junit:4.13.2'
           Dependency path 'Sakamichi app:app:unspecified' --> 'androidx.test.ext:junit:1.1.3' (runtime) --> 'junit:junit:4.12'
           Dependency path 'Sakamichi app:app:unspecified' --> 'com.squareup.okhttp3:mockwebserver:4.9.1' (runtimeElements) --> 'junit:junit:4.13'
           Dependency path 'Sakamichi app:app:unspecified' --> 'androidx.compose.ui:ui-test-junit4:1.0.1' (releaseVariantReleaseRuntimePublication) --> 'junit:junit:4.12'
           Dependency path 'Sakamichi app:app:unspecified' --> 'androidx.test.espresso:espresso-core:3.4.0' (runtime) --> 'androidx.test:runner:1.4.0' (runtime) --> 'junit:junit:4.12'

   > Could not resolve junit:junit:4.13.
     Required by:
         project :app > com.google.dagger:hilt-android-testing:2.37
         project :app > com.squareup.okhttp3:mockwebserver:4.9.1
      > Cannot find a version of 'junit:junit' that satisfies the version constraints:
           Dependency path 'Sakamichi app:app:unspecified' --> 'junit:junit:4.13.2'
           Constraint path 'Sakamichi app:app:unspecified' --> 'junit:junit:{strictly 4.12}' because of the following reason: debugRuntimeClasspath uses version 4.12
           Dependency path 'Sakamichi app:app:unspecified' --> 'com.google.dagger:hilt-android-testing:2.37' (runtime) --> 'junit:junit:4.13'
           Dependency path 'Sakamichi app:app:unspecified' --> 'androidx.arch.core:core-testing:2.1.0' (runtime) --> 'junit:junit:4.12'
           Dependency path 'Sakamichi app:app:unspecified' --> 'com.google.truth:truth:1.1.3' (runtime) --> 'junit:junit:4.13.2'
           Dependency path 'Sakamichi app:app:unspecified' --> 'androidx.test.ext:junit:1.1.3' (runtime) --> 'junit:junit:4.12'
           Dependency path 'Sakamichi app:app:unspecified' --> 'com.squareup.okhttp3:mockwebserver:4.9.1' (runtimeElements) --> 'junit:junit:4.13'
           Dependency path 'Sakamichi app:app:unspecified' --> 'androidx.compose.ui:ui-test-junit4:1.0.1' (releaseVariantReleaseRuntimePublication) --> 'junit:junit:4.12'
           Dependency path 'Sakamichi app:app:unspecified' --> 'androidx.test.espresso:espresso-core:3.4.0' (runtime) --> 'androidx.test:runner:1.4.0' (runtime) --> 'junit:junit:4.12'
...
```

## 解決策
`build.gralde` の中に、次のような設定（configurations）を記述します。

依存関係の衝突がが起きた時に、無理矢理使うバージョンを指定するためのものだと理解しています。（新しいものの方がいいだろう、というノリで 4.13.2 の方を選択しました。）

```gradle
android {
    packagingOptions {
        ...
    }
    configurations.all {
        resolutionStrategy {
            force 'junit:junit:4.13.2'
        }
    }
}
```


## 参考サイト
[Could not resolve org.hamcrest:hamcrest-core:{strictly 1.3} Required by: project :TestApp(stack overflow)](https://stackoverflow.com/questions/69756393/could-not-resolve-org-hamcresthamcrest-corestrictly-1-3-required-by-project)

## おわりに
今回は androidTest を走らせようとした際に起こった、依存性の衝突の回避方法について紹介しました。

gradle の部分は毎回コピペで済ませてしまっているので、いつか理解したいと思います。
