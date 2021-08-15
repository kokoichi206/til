package io.kokoichi.sample.databasesample

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.*

class MainActivity : AppCompatActivity() {
    /**
     * 選択されたカクテルの主キーIDを表すフィールド
     */
    private var _cocktailId = -1

    /**
     * 選択されたカクテル名を表すフィールド
     */
    private var _cocktailName = ""

    // データベースヘルパーオブジェクト
    private val _helper = DatabaseHelper(this@MainActivity)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // カクテルリスト用ListView(lvCocktail)を取得
        val lvCocktail = findViewById<ListView>(R.id.lvCocktail)
        lvCocktail.onItemClickListener = ListItemClickListener()
    }

    /**
     * 保存ボタンがタップされた時の処理メソッド
     */
    fun onSaveButtonClick(view: View) {
        // 感想欄を取得
        val etNote = findViewById<EditText>(R.id.etNote)
        // 入力された感想を取得
        val note = etNote.text.toString()

        // DBヘルパーオブジェクトからDB接続オブジェクトを取得
        val db = _helper.writableDatabase

        // まず、リストで選択されたカクテルのメモデータを削除。その後インサート
        val sqlDelete = "DELETE FROM cocktailmemos WHERE _id = ?"
        // SQL文字列を元にプリペアドステートメントを取得
        var stmt = db.compileStatement(sqlDelete)
        // 変数のバイト
        stmt.bindLong(1, _cocktailId.toLong())
        // 削除用SQLの実行
        stmt.executeUpdateDelete()

        // インサート用SQL文字列の用意
        val sqlInsert = "INSERT INTO cocktailmemos (_id, name, note) VALUES (?, ?, ?)"
        // SQL文字列を元にプリペアドステートメントを取得
        stmt = db.compileStatement(sqlInsert)
        // 変数のバイト
        stmt.bindLong(1, _cocktailId.toLong())
        stmt.bindString(2, _cocktailName)
        stmt.bindString(3, note)
        // インサートSQLの実行
        stmt.executeInsert()

        etNote.setText("")
        val tvCocktailName = findViewById<TextView>(R.id.tvCocktailName)
        tvCocktailName.text = getString(R.string.tv_name)
        val btnSave = findViewById<Button>(R.id.btnSave)
        // 保存ボタンをタップできないように変更
        btnSave.isEnabled = false
    }

    /**
     * リストがタップされた時の処理が記述されたメンバクラス
     */
    private inner class ListItemClickListener : AdapterView.OnItemClickListener {
        override fun onItemClick(parent: AdapterView<*>, view: View, position: Int, id: Long) {
            // タップされた行番号をフィールドの主キーIDに代入
            _cocktailId = position
            // タップされた行のデータを取得
            _cocktailName = parent.getItemAtPosition(position) as String
            val tvCocktailName = findViewById<TextView>(R.id.tvCocktailName)
            tvCocktailName.text = _cocktailName
            val btnSave = findViewById<Button>(R.id.btnSave)
            btnSave.isEnabled = true

            /**
             * DBにすでに登録がある場合は、それを表示する
             */
            val db = _helper.writableDatabase
            // 主キーによる検索SQL文字列の用意
            val sql = "SELECT * FROM cocktailmemos WHERE _id = ${_cocktailId}"
            // SQLの実行
            var cursor = db.rawQuery(sql, null)

            var note = ""
            // SQL実行の戻り値であるカーソルオブジェクトをループさせて、DB内のデータを取得
            while(cursor.moveToNext()) {
                // カラムのインデックス値を取得
                val idxNote = cursor.getColumnIndex("note")
                // カラムのインデックス値を元に実際のデータを取得
                note = cursor.getString(idxNote)
            }
            // 感想のEditTextの各画面部分を取得しDBの値を反映
            val etNote = findViewById<EditText>(R.id.etNote)
            etNote.setText(note)
        }
    }

    override fun onDestroy() {
        // ヘルパーオブジェクトの開放
        _helper.close()
        super.onDestroy()
    }
}