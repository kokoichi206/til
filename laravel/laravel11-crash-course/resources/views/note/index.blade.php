<x-layout>
    <div class="note-container">
        <a href="{{ route('note.') }}" class="new-note-btn">
            New Note!
        </a>
        <div class="notes">
            @foreach ($notes as $note)
                <div class="note">
                    <div class="note-body">
                        {{ Str::words($note->note, 30) }}
                    </div>
                    <div class="note-buttons">
                        <a href="{{ route('note.show', $note) }}" class="note-edit-button">View</a>
                        <a href="{{ route('note.edit', $note) }}" class="note-edit-btn">Edit</a>
                        <button href="#" class="note-delete-btn">Delete</button>
                    </div>
                </div>
            @endforeach
        </div>
    </div>
</x-layout>
