let currentIndex = 0;
let currentQuery = '';
let debounceTimeout;

function searchSongs(reset = false) {
    const query = document.getElementById('songQuery').value;
    if (!query) {
        document.getElementById('results').innerHTML = `
            <div class="bg-red-500/20 text-red-400 p-4 rounded-lg">
                Please enter a song or artist.
            </div>
        `;
        return;
    }

    // Reset pagination if new query
    if (reset || query !== currentQuery) {
        currentIndex = 0;
        currentQuery = query;
        document.getElementById('results').innerHTML = '';
    }

    // Show loading spinner
    document.getElementById('loading').classList.remove('hidden');

    fetch(`/search?q=${encodeURIComponent(query)}&index=${currentIndex}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            const loadingDiv = document.getElementById('loading');
            loadingDiv.classList.add('hidden');

            if (data.error) {
                resultsDiv.innerHTML = `
                    <div class="bg-red-500/20 text-red-400 p-4 rounded-lg">
                        ${data.error}
                    </div>
                `;
                return;
            }

            if (data.songs.length > 0) {
                data.songs.forEach(song => {
                    const songElement = document.createElement('div');
                    songElement.className = 'song-card bg-white/10 p-4 rounded-lg';
                    songElement.innerHTML = `
                        <img src="${song.cover_small}" alt="${song.album}" class="w-full h-32 object-cover rounded mb-4">
                        <h3 class="font-semibold">${song.title}</h3>
                        <p class="text-gray-300">${song.artist}</p>
                        <p class="text-gray-400 text-sm">${song.album}</p>
                        <button
                            onclick="playPreview('${song.preview}')"
                            class="mt-4 bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded transition"
                            aria-label="Play preview of ${song.title}"
                        >
                            Play Preview
                        </button>
                    `;
                    resultsDiv.appendChild(songElement);
                });

                // Update pagination
                const paginationDiv = document.getElementById('pagination');
                if (data.next_index) {
                    paginationDiv.innerHTML = `
                        <button
                            onclick="loadMore()"
                            class="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition"
                            aria-label="Load more songs"
                        >
                            Load More
                        </button>
                    `;
                } else {
                    paginationDiv.innerHTML = '';
                }
                currentIndex = data.next_index;
            } else {
                if (currentIndex === 0) {
                    resultsDiv.innerHTML = `
                        <div class="bg-gray-500/20 text-gray-300 p-4 rounded-lg">
                            No results found.
                        </div>
                    `;
                }
                paginationDiv.innerHTML = '';
            }
        })
        .catch(error => {
            console.error('Error fetching songs:', error);
            document.getElementById('loading').classList.add('hidden');
            document.getElementById('results').innerHTML = `
                <div class="bg-red-500/20 text-red-400 p-4 rounded-lg">
                    Error loading results. Please try again.
                </div>
            `;
        });
}

function loadMore() {
    searchSongs();
}

function playPreview(previewUrl) {
    const player = document.getElementById('player');
    player.src = previewUrl;
    player.play().catch(error => {
        console.error('Playback error:', error);
        document.getElementById('results').innerHTML = `
            <div class="bg-red-500/20 text-red-400 p-4 rounded-lg">
                Error playing preview. Try another song.
            </div>
        `;
    });
}

function clearSearch() {
    document.getElementById('songQuery').value = '';
    document.getElementById('results').innerHTML = '';
    document.getElementById('pagination').innerHTML = '';
    currentIndex = 0;
    currentQuery = '';
}

// Debounce search on input
document.getElementById('songQuery').addEventListener('input', () => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => searchSongs(true), 500);
});