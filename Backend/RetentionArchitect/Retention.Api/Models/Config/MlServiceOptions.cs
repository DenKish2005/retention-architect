namespace Retention.Api.Models.Config;

public class MlServiceOptions
{
    public string BaseUrl { get; set; } = string.Empty;
    public int TimeoutSeconds { get; set; } = 30;
}