// 초기 진입 시 포커스
$(document).ready(function () {
    $("#search-title").focus();
});

// 검색어와 일치하는 영화 리스트 조회
function getMatches() {
    let searchTitle = $("#search-title").val();

    // 검색어 예외 처리
    if (searchTitle == ""){
        alert('검색어를 입력하세요');
        return false;
    } else {
        // 검색어 보내기
        $.ajax({
            type: "GET",
            url: "/search",
            data: {title_give: searchTitle},
            success: function (response) {
                let matchList = response['match_list']

                if (matchList == ""){
                    $('#searchList').hide();
                    $('.nodata').show();

                    let nodataOffset = $('.nodata').offset();
                    $('html').animate({scrollTop: nodataOffset.top}, 400);

                    return false;
                } else{
                    // 검색 결과 섹션 비우기
                    $('.nodata').hide();
                    $('#searchList').empty().show();

                    // 검색 결과로 스크롤 다운
                    let searchListOffset = $('#searchList').offset();
                    $('html').animate({scrollTop: searchListOffset.top}, 400);

                    // 일치 영화 리스트 보여주기
                    for (let i = 0; i < matchList.length; i++) {
                        let matchFilm = matchList[i];
                        let filmId = matchFilm['id']
                        let filmTitle = matchFilm['title']
                        let posterUrl = matchFilm['poster_url']
                        let temp = `
                                <li class="card">
                                    <a href="/film_detail?id_give=${filmId}" onclick="showDetail(${filmId})" title="${filmTitle}">
                                        <div class="img-area">
                                            <img src="https://images.justwatch.com${posterUrl}">
                                        </div>
                                    </a>
                                </li>
                            `;
                        $('#searchList').append(temp);
                    }
                }
            }
        })
    }


}

// 검색 키다운
const searchScrollDown = function () {
    const $searchInput = $('.search-input');

    $searchInput.on('keydown', function (k) {
        if (k.keyCode === 13) {
            getMatches();
        }
    });
}

// 디테일 페이지 요청
function showDetail(filmId) {
    // event.preventDefault();
    $.ajax({
        type: "GET",
        url: "/film_detail",
        data: {id_give: filmId},
        success: function (response) {
            let infos = response['id_receive']
            console.log(infos);

            // 디테일 영화 인포 보여주기

        }
    })
}

// 위시리스트
const makeWishlist = function () {
    const $wishBtn = $('.add-wishlist');
    const $wishId = $wishBtn.data('id');
    const $wishPoster = $wishBtn.data('poster');
    const $wishTitle = $wishBtn.data('title');
    const $this = $(this);

    $wishBtn.on('click', function (e) {
        e.preventDefault();
        if ($wishBtn.hasClass('active') === false) {
            let wishlists = {
                id : $wishId,
                poster : $wishPoster,
                title : $wishTitle
            }

            window.localStorage.setItem($wishId, JSON.stringify(wishlists));
            window.location.reload();
        } else if($wishBtn.hasClass('active')) {
            $wishBtn.removeClass('active');
            $('.wishlist-icon').attr('src', '../static/images/icon_wish.png');

            window.localStorage.removeItem($wishId);
            window.location.reload();
        }
    })

    // Check for saved wishlist items
    for(let i =0; i < localStorage.length; i++){
       // console.log(localStorage.getItem(localStorage.key(i)));
       let saved = localStorage.getItem(localStorage.key(i));
       saved = JSON.parse(saved)
       console.log(saved)
       if (saved != null && saved.length != 0) {
            let temp = `
                    <li class="card">
                        <a href="/film_detail?id_give=${saved.id}" onclick="showDetail(${saved.id})" title="${saved.title}">
                            <div class="img-area">
                                <img src="https://images.justwatch.com${saved.poster}">
                            </div>
                        </a>
                    </li>
                `;
            $('#wishList').append(temp);
        }
        // saved wishlist film active
        if (saved.id == $wishId) {
            $wishBtn.addClass('active');
            $('.wishlist-icon').attr('src', '../static/images/icon_wish_on.png');
        }
    }
}

searchScrollDown();
makeWishlist();
