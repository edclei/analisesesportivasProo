/* dev proxy helper: in production configure proper proxy or use same origin */
import axios from 'axios';
export default axios.create({ baseURL: '/' });
