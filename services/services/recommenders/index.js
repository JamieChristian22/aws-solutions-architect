// services/recommenders/index.js
exports.handler = async () => {
  // Placeholder: return a few static recommendations to start
  return {
    statusCode: 200,
    body: JSON.stringify({
      recommendations: [
        { sku: 'SKU-001', reason: 'popular' },
        { sku: 'SKU-002', reason: 'similar_to_last_view' }
      ]
    })
  };
};
