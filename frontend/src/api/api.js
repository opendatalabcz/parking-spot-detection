const axios = require('axios');
class Api {
    BACKEND_URL = "http://localhost:8000/"
    BASE_URL = this.BACKEND_URL + "api/";
    LOT_DETAIL = this.BASE_URL+"lot/";
    getLotSpotsUrl = (lotId) => this.BASE_URL+`lot/${lotId}/spot/`;
    getLotSettingsUrl = (lotId) => this.BASE_URL+`lot/${lotId}/settings/`;
    getLotHistoryUrl = (lotId) => this.BASE_URL+`lot/${lotId}/history/`;
    getSpotHistoryUrl = (lotId, spotId) => this.BASE_URL+`lot/${lotId}/spot/${spotId}/history/`;
    getSnapshotUrl = lotId => this.BASE_URL+`lot/${lotId}/snapshot/`
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
    getLotHistory = (lotId) => axios.get(this.getLotHistoryUrl(lotId));
    getSpotHistory = (lotId, spotId) => axios.get(this.getSpotHistoryUrl(lotId, spotId));
    createLot = (data) => {
        const params = new URLSearchParams();
        params.append("data", JSON.stringify(data));
        return axios({
            url: this.LOT_DETAIL,
            method: "post",
            data: params
        });
    };
    saveSettings = (lotId, data) => {
        const params = new URLSearchParams();
        params.append("data", JSON.stringify(data));
        return axios({
                url: this.getLotSettingsUrl(lotId),
                method: 'post',
                data: params
            });
    };
    getLotSettings = (lotId) => axios.get(this.getLotSettingsUrl(lotId));



}

module.exports = new Api();