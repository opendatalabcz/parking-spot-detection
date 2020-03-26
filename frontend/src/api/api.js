const axios = require('axios');
class Api {
    BASE_URL = "http://localhost:8000/api/";
    BASE_MEDIA_URL = "http://localhost:8000/media/";

    LOT_DETAIL = this.BASE_URL+"lot/";
    getLotSpotsUrl = (lotId) => this.BASE_URL+`lot/${lotId}/spot/`;


    fetchImage = (url) => axios.get(this.BASE_MEDIA_URL+url);
    getLotDetail = (id) => axios.get(this.LOT_DETAIL+id);
    getLots = () => axios.get(this.LOT_DETAIL);
    getLotSpots = (lotId) => axios.get(this.getLotSpotsUrl(lotId));

    getImageUrl = url => this.BASE_MEDIA_URL+url;


}

module.exports = new Api();