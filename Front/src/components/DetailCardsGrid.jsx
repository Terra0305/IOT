// src/components/DetailCardsGrid.jsx (수정)

// ... (DUMMY_DETAIL_DATA 정의는 그대로 둡니다. 단, 배열의 순서를 조정합니다.)

// DUMMY_DETAIL_DATA가 [UV, Wind, Humidity, Dust] 순서라고 가정합니다.
const DUMMY_DETAIL_DATA_PAIRS = [
    { dataA: DUMMY_DETAIL_DATA[0], dataB: DUMMY_DETAIL_DATA[1] }, // UV + Wind
    { dataA: DUMMY_DETAIL_DATA[2], dataB: DUMMY_DETAIL_DATA[3] }  // Humidity + Dust
];

function DetailCardsGrid() {
    return (
        <div className="detail-grid-container">
            {
                DUMMY_DETAIL_DATA_PAIRS.map((pair, index) => (
                    <DetailCard
                        key={index}
                        dataA={pair.dataA} // UV or Humidity
                        dataB={pair.dataB} // Wind or Dust
                    />
                ))
            }
        </div>
    );
}

export default DetailCardsGrid;