
function getMonetizationType(type){
    if(type === 'buy'){
        return '구매'
    }
}

function getMonetizationType(type){
    switch(type){
        case 'buy':
            return '구매';
        case 'rent':
        return '구매';
    }
}

var monetizationType = {
    buy: '구매',
    rent: '렌트'
}


var data = {offers: []}

var filteredData = data.offers.map((offer) => {
    return {
        monetization_type: monetizationType[offer.monetization_type],
        provider_id: offer.provider_id,
        urls_standard_web: offer.urls.standard_web
    }
});

