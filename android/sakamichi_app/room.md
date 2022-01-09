## entities
each entity is each table

kotlin class

```kotlin
@Entity
data class Director(
    @PrimaryKey(autoGenerate = false)
    val directorName: String,
    val schoolName: String
)

@Entity
data class School(
    @PrimaryKey(autoGenerate = false)
    val schroolName: String
)
```

```kotlin
// parent and entity
data class SchoolAndDirector(
    @Embedded val school: School,
    @Relation(
        parentColumn = "schoolName",
        entityColumn = "schoolName"
    )
    val director: Director
)
```


entities
| - relations
| | - SchoolAndDirector
| - Director
| - School
| - 

```kotlin
@Dao
interface SchroolDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSchrool(school: School)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertDirector(director: Director)

    @Transaction
    @Query("SELECT * FROM school WHERE schoolName = :schoolName")
    suspend fun getSchoolAndDirectorWithSchoolName(schoolName: String): List<SchoolAndDirector>
}
```



```
java.lang.IllegalStateException: Cannot access database on the main thread since it may potentially lock the UI for a long period of time.
```


