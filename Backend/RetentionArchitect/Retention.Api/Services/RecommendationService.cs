using Retention.Api.Models.Responses;

namespace Retention.Api.Services;

public class RecommendationService
{
    public List<string> BuildFallbackRecommendations(PredictionResponse prediction)
    {
        var recommendations = new List<string>();

        if (prediction.ChurnProbability >= 0.8)
        {
            recommendations.Add("Escalate this user to a high-priority retention flow.");
        }

        if (prediction.PredictedClass.Equals("involuntary_churn", StringComparison.OrdinalIgnoreCase))
        {
            recommendations.Add("Ask the user to update their payment method.");
            recommendations.Add("Trigger a smart payment retry flow.");
        }

        if (prediction.PredictedClass.Equals("voluntary_churn", StringComparison.OrdinalIgnoreCase))
        {
            recommendations.Add("Send a personalized retention offer.");
            recommendations.Add("Collect feedback about dissatisfaction reasons.");
        }

        if (recommendations.Count == 0)
        {
            recommendations.Add("Continue monitoring this user.");
        }

        return recommendations;
    }
}