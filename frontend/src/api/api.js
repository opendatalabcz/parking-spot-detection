const axios = require('axios');
class Api {
    BASE_URL = "http://localhost:8000/api/";
    BASE_MEDIA_URL = "http://localhost:8000/media/";

    LOT_DETAIL = this.BASE_URL+"lot/";
    LOT_RECTS = this.BASE_URL+"lot_rects/";


    fetchImage = (url, cb) => axios.get(this.BASE_MEDIA_URL+url).then(r => cb(r.data));
    getLotDetail = (id, cb) => axios.get(this.LOT_DETAIL+id).then(r => cb(r.data));
    getLots = (cb) => axios.get(this.LOT_DETAIL).then(r => cb(r.data));
    getLotRects = (id, cb) => axios.get(this.LOT_RECTS+id).then( r => cb(r.data))

    getImageUrl = url => this.BASE_MEDIA_URL+url
}

module.exports = new Api();