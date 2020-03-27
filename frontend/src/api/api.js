const axios = require('axios');
class Api {
    BASE_URL = "http://localhost:8000/api/";
    BASE_MEDIA_URL = "http://localhost:8000/media/";

    LOT_DETAIL = this.BASE_URL+"lot/";
    getLotSpotsUrl = (lotId) => this.BASE_URL+`lot/${lotId}/spot/`;
    getLotHistoryUrl = (lotId) => this.BASE_URL+`lot/${lotId}/history/`;


    fetchImage = (url) => axios.get(this.BASE_MEDIA_URL+url);
    getLotDetail = (id) => axios.get(this.LOT_DETAIL+id);
    getLots = () => axios.get(this.LOT_DETAIL);
    getLotSpots = (lotId) => axios.get(this.getLotSpotsUrl(lotId));
    uploadSpots = (lotId, data) => {
        const params = new URLSearchParams();
        params.append("data", JSON.stringify(data));
        return axios({
                url: this.getLotSpotsUrl(lotId),
                method: 'post',
                data: params
            });
    };
    getImageUrl = url => this.BASE_MEDIA_URL+url;
    getLotHistory = (lotId) => axios.get(this.getLotHistoryUrl(lotId))


}

module.exports = new Api();