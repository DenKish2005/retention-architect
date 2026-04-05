namespace Retention.Api.Models.Responses;

public class PredictionResponse
{
    public string UserId { get; set; } = string.Empty;
    public double ChurnProbability { get; set; }
    public string PredictedClass { get; set; } = string.Empty;
    public ClassProbabilitiesDto? ClassProbabilities { get; set; }
    public List<string> TopDrivers { get; set; } = new();
    public List<ExplanationDto> Explanations { get; set; } = new();
    public List<string> RecommendedActions { get; set; } = new();
}