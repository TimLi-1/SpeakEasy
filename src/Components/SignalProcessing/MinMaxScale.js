
export default ({s}) => {
    const sMin = Math.min(...s);
    const sMax = Math.max(...s);
    const scale = 1 / (sMax - sMin);
    return s.map(si => (scale * si) - (sMin * scale));
}