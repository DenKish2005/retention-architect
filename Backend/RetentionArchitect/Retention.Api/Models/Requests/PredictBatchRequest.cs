namespace Retention.Api.Models.Requests;

public class PredictBatchRequest
{
    public List<string> UserIds { get; set; } = new();
}