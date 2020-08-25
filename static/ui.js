
// 검색어와 일치하는 영화 리스트 조회
function getMatches() {
    $('#searchList').empty().show();

    // 검색 결과로 스크롤 다운
    let offset = $('#searchList').offset();
    $('html').animate({scrollTop : offset.top}, 400);

    let searchTitle = $("#search-title").val();

    $.ajax({
        type: "GET",
        url: "/search",
        data: {title_give: searchTitle},
        success: function (response) {
            let matchList = response['match_list']

            // 일치 영화 리스트 보여주기
            for (let i = 0; i < matchList.length; i++) {
                let matchFilm = matchList[i];
                let filmId = matchFilm['id']
                let filmTitle = matchFilm['title']
                let posterUrl = matchFilm['poster_url']
                let temp = `
                        <li class="card">
                            <a href="/film_detail" onclick="showDetail(${filmId})" title="${filmTitle}">
                                <div class="img-area">
                                    <img src="https://images.justwatch.com${posterUrl}">
                                </div>
                            </a>
                        </li>
                    `;
                $('#searchList').append(temp);
            }
        }
    })
}

// 검색 키다운
let searchInput = $('.search-input');
searchInput.on('keydown', function (k) {
    if (k.keyCode === 13) {
        getMatches();
    }
});

// 디테일 페이지 요청
function showDetail(filmId) {
    // event.preventDefault();
    $.ajax({
        type: "GET",
        url: "/film_detail",
        data: {id_give : filmId},
        success: function (response) {
            let infos = response['id_receive']
            // console.log(infos);
            // 디테일 영화 인포 보여주기

        }
    })
}



